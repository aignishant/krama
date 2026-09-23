---
day: 81
track: dsa
title: "Reversing a linked list"
phase: "Linked lists"
status: written
---

# Day 081 · DSA — Reversing a linked list

**After today you can:** You can reverse a list iteratively and recursively and draw the pointer moves.

**The interviewer asks it as:** *Reverse a linked list. Now do it in groups of k.*

---

## 1. What this is, and why they ask it

Reversing a linked list means turning every arrow round. `1 → 2 → 3 → None` becomes
`None ← 1 ← 2 ← 3`, so the old tail is the new head. No node moves, no node is created, no value is
copied. You change `next` on each node exactly once.

The whole difficulty is one line long. The moment you overwrite `current.next`, **you have destroyed
your only way of reaching the rest of the list** — so you must save it first. Three variables and four
lines, in a fixed order, and the order is not negotiable.

They ask it constantly. It is the most-asked linked list question there is, it is asked as a warm-up
before something harder, and it is asked because a candidate either has the three-pointer dance in
their fingers or does not. The follow-ups are predictable and they escalate: do it recursively, reverse
only the middle section, reverse in groups of k. Every one of those is this loop wrapped in something,
so the ten minutes you spend making this automatic pay for the rest of the phase.

---

## 2. The story

The trip to the caves was Nalini's class, thirty-one children, and the path in was narrow enough that
they had to go single file.

She lined them up the way she always does. Each child takes hold of the bag strap of the child in
front. Nobody holds anybody's hand — hands get pulled away — but a bag strap you can hold for an hour.
Anil at the front, holding nothing, walking beside her.

Two hundred metres in, the path stopped. There was a gate across it, chained, and a board that had
been there long enough to be unreadable. The path did not go through. They had to go back out the way
they had come.

There was no room to turn around as a group. The path was a metre wide with rock on one side.

So Nalini turned the line inside out, and she did it from the front, one child at a time.

She started with Anil, who was now at the wrong end. She told him: look behind you, see who is there —
that is Farida — let go of nothing, because you are holding nothing, and take hold of Farida's strap.
Then Farida: look behind you first, that is Kiran, then let go of Anil's strap, then take hold of
Kiran's. Then Kiran, the same. Look back, let go, take hold.

The order was the whole thing, and she said it in that order every single time, thirty-one times,
because of what happened on a trip four years ago. A boy let go first and then looked behind him, and
in the two seconds in between, the child behind him had stopped to look at something and there was a
gap, and the boy could not see who he was supposed to take hold of. The back two-thirds of the line —
nineteen children — simply stood there, holding each other, no longer attached to anything at the
front. Nalini did not notice for four minutes.

So now it is always: **look behind you first. Then let go. Then take hold.**

At the end, the child who had been at the back was at the front, and she was holding nothing, which is
how you know the line is finished. Nalini walked to that end and led them out.

---

## 3. The idea in plain English

Nalini's three-step instruction is the algorithm. **Look behind you, let go, take hold** — in that
order, and the reason for the order is the boy who lost nineteen children.

### The three variables

```python
    previous = None        # the child behind me, whose strap I will take
    current = head         # me
    next_node = None       # the child in front of me, saved before I let go
```

`previous` starts as `None` because the first node has nobody behind it, and in the reversed list the
old head has nothing after it — it becomes the tail. That single `None` is doing two jobs and it is
worth noticing.

### The four lines, in the only order that works

```python
    while current is not None:
        next_node = current.next        # 1. look behind you (save the rest of the list)
        current.next = previous         # 2. let go, take hold (turn the arrow round)
        previous = current              # 3. previous moves up
        current = next_node             # 4. current moves up
    return previous                     # previous is the new head
```

Line 1 is the one that matters. `current.next` is overwritten by line 2, so if you have not saved it,
the entire remainder of the list is unreachable — the nineteen children standing in the path. Every
other bug in this problem is small; this one loses everything.

**Return `previous`, not `head`.** When the loop ends, `current` is `None` and `previous` is the last
node visited, which is the old tail and the new head. `head` still refers to the old first node, which
is now the last one. Returning it gives you a one-element list.

### Why it is O(1) space

Nothing is copied and nothing is allocated. Three references, whatever the length. Contrast with the
tempting alternative — read all the values into a Python list, reverse it, and rebuild — which is O(n)
extra space and is a legitimate answer only if you say out loud that you are trading space for
simplicity.

### The recursive version, and the two lines that look like magic

```python
def reverse_recursive(head):
    if head is None or head.next is None:
        return head                     # base case: empty, or a single node
    new_head = reverse_recursive(head.next)
    head.next.next = head               # the node after me now points AT me
    head.next = None                    # and I point at nothing
    return new_head
```

The trick to reading it is to trust the recursive call, which is exactly the habit
[day 087](../day-087-recursion-leap-of-faith/README.md) will make explicit. Assume
`reverse_recursive(head.next)` has already reversed everything after `head`, and returned the new head
of that reversed part.

Now you are standing on `head`, and `head.next` still points at what *was* the second node — which is
now the **last** node of the reversed part. So:

- `head.next.next = head` makes that last node point back at you. You are attached to the end.
- `head.next = None` makes you the new tail.
- `new_head` is unchanged all the way up, because the new head is the old tail and it was found at the
  very bottom of the recursion.

**Do not skip `head.next = None`.** Without it, the old head still points forward at the node that now
points back at it, and you have built a two-node cycle. Printing the result never returns.

Say the cost honestly: this is O(n) stack space, and Python's recursion limit is 1000, so a list of
ten thousand nodes raises. The iterative version is strictly better, and the recursive one is worth
knowing because interviewers ask for it and because it is the shape of every tree problem later.

### Reversing only part of the list

*Reverse the nodes between positions m and n.* This is where the dummy head from
[day 080](../day-080-dummy-head/README.md) earns itself again, because m may be 1 and then the head
changes.

The method is: walk to the node just before position m, hold it, reverse the sublist with the same
four lines, then reattach both ends.

```
 before:  1 -> 2 -> 3 -> 4 -> 5,  reverse positions 2..4
          ^         (this is `before`, the node at position 1)

 after:   1 -> 4 -> 3 -> 2 -> 5
```

The two reattachments are where it goes wrong: `before.next` must become the last node of the
reversed section, and the **first** node of the original section — which is now the last — must point
at whatever followed the section. Hold that first node in a variable before you start, because after
the reversal you cannot find it.

### Reversing in groups of k

*Reverse every consecutive group of k nodes; leave a final group of fewer than k alone.*

Three parts, and the third is the one people forget:

1. **Check there are k nodes left**, by walking ahead. If not, stop and leave the rest as it is.
2. Reverse those k with the same four lines, stopping after exactly k steps.
3. **Reattach**: the node before the group points at the group's new first node, and the group's new
   last node points at whatever comes next.

The check must happen *before* the reversal, not after. If you reverse first and then discover there
were only three nodes when k is four, you have to reverse them back — which is legal, and is
embarrassing, and is not what anyone wants to watch.

---

## 4. The picture

Reversing `1 → 2 → 3`. Watch `next_node`, which exists only to survive line 2.

```
 start
   previous = None
   current  = [1] -> [2] -> [3] -> None

 --- iteration 1 ---
   1. next_node = current.next            next_node = [2]
   2. current.next = previous             [1] -> None
   3. previous = current                  previous = [1]
   4. current = next_node                 current  = [2]

   None <- [1]        [2] -> [3] -> None
            ^          ^
        previous     current

 --- iteration 2 ---
   next_node = [3];  [2] -> [1];  previous = [2];  current = [3]

   None <- [1] <- [2]        [3] -> None
                   ^          ^
               previous     current

 --- iteration 3 ---
   next_node = None; [3] -> [2];  previous = [3];  current = None

   None <- [1] <- [2] <- [3]
                          ^
                      previous          current is None: stop

 return previous  ->  [3] -> [2] -> [1] -> None
```

What to notice: after line 2 of the first iteration, **nothing in the world points at node 2 except
`next_node`.** Node 1's arrow has already been turned round. That one variable is the only thing
standing between you and losing the list, which is why it is written first and why Nalini says "look
behind you" first every time.

And the recursive version, drawn at the moment it does its work:

```
 the call stack has unwound to head = [1], and everything after is already reversed

   [1] -----------> [2] <- [3]          head.next is still [2]
    ^                ^      ^           and [2] is now the LAST node
   head          head.next  new_head

   head.next.next = head    ->   [2] -> [1]
   head.next = None         ->   [1] -> None

   result:  [3] -> [2] -> [1] -> None

 forget `head.next = None` and you get:

   [1] -> [2] -> [1] -> [2] -> ...      a two-node cycle, printing never returns
```

---

## 5. The code, built step by step

### Step 1 — the three variables, and what each is for

```python
    previous: Node | None = None       # becomes the new head; None makes the old head a tail
    current: Node | None = head        # the node whose arrow we are about to turn
```

Two, not three, at the start — `next_node` is created inside the loop because it only has to survive
one iteration.

### Step 2 — the loop, in the fixed order

```python
    while current is not None:
        next_node = current.next       # SAVE FIRST. Everything else depends on this.
        current.next = previous
        previous = current
        current = next_node
```

Read them out loud as you type: *save, turn, previous up, current up.* Four lines, always the same,
and if you write them in any other order something is lost.

### Step 3 — the return

```python
    return previous
```

`current` is `None` and `previous` is the last node visited. That is the old tail, and the old tail is
the new head.

### Step 4 — reversing a sublist, with a dummy

```python
    dummy = Node(0, head)
    before = dummy
    for _ in range(left - 1):          # walk to the node just before position `left`
        before = before.next
```

The dummy means `left == 1` needs no special case: `before` is simply the dummy itself.

```python
    tail_of_reversed = before.next     # this node ends up LAST — hold it now
    previous, current = None, before.next
    for _ in range(right - left + 1):  # reverse exactly this many nodes
        next_node = current.next
        current.next = previous
        previous = current
        current = next_node
```

`tail_of_reversed` must be captured **before** the reversal, because afterwards there is no way to
find it. This is the line people leave out and then spend five minutes hunting for.

```python
    before.next = previous             # attach the reversed section
    tail_of_reversed.next = current    # and its far end to the remainder
    return dummy.next
```

Two reattachments, in either order, and both are required.

### Step 5 — groups of k, with the check first

```python
    def has_k_nodes(node, k):
        for _ in range(k):
            if node is None:
                return False
            node = node.next
        return True
```

A separate walk, before touching anything. It costs another O(n) across the whole run — so the
algorithm is O(2n), still linear — and it buys you never having to undo a reversal.

### The complete solution

```python
class Node:
    __slots__ = ("value", "next")

    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value
        self.next = next


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
    """Reverse the list in place. O(n) time, O(1) space.

    The order of the four lines is not negotiable: current.next is overwritten
    on line 2, so the rest of the list must be saved on line 1 or it is lost.

    Returns `previous`, not `head` — the old tail is the new head.
    """
    previous: Node | None = None
    current = head

    while current is not None:
        next_node = current.next       # 1. save the rest of the list
        current.next = previous        # 2. turn this arrow round
        previous = current             # 3. step previous forward
        current = next_node            # 4. step current forward

    return previous


def reverse_recursive(head: Node | None) -> Node | None:
    """The same thing recursively. O(n) time, O(n) STACK space.

    Trust the recursive call: assume everything after `head` is already
    reversed. Then head.next is the last node of that reversed part, so point
    it back at head, and make head the new tail.

    Python's recursion limit is 1000, so this raises on a long list.
    """
    if head is None or head.next is None:
        return head                    # empty or single node: already reversed

    new_head = reverse_recursive(head.next)
    head.next.next = head              # the node after me now points at me
    head.next = None                   # and I point at nothing — MANDATORY
    return new_head                    # unchanged all the way up


def reverse_between(head: Node | None, left: int, right: int) -> Node | None:
    """Reverse positions left..right (1-indexed), leaving the rest alone.

    The dummy removes the left == 1 case. `tail_of_reversed` must be captured
    BEFORE the reversal — afterwards there is no way to find it.
    """
    if head is None or left >= right:
        return head

    dummy = Node(0, head)
    before = dummy
    for _ in range(left - 1):
        before = before.next

    tail_of_reversed = before.next     # ends up last; hold it now
    previous, current = None, before.next
    for _ in range(right - left + 1):
        next_node = current.next
        current.next = previous
        previous = current
        current = next_node

    before.next = previous             # front joint
    tail_of_reversed.next = current    # back joint
    return dummy.next


def reverse_k_group(head: Node | None, k: int) -> Node | None:
    """Reverse every consecutive group of k nodes. A final group of fewer than
    k is left as it is.

    The count check happens BEFORE the reversal, so a short final group is
    never reversed and then un-reversed.
    """
    if k <= 1:
        return head

    dummy = Node(0, head)
    group_before = dummy

    while _has_k_nodes(group_before.next, k):
        group_start = group_before.next        # becomes the group's LAST node
        previous, current = None, group_start
        for _ in range(k):
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        group_before.next = previous           # attach the reversed group
        group_start.next = current             # and its far end to the rest
        group_before = group_start             # next group starts after this

    return dummy.next


def _has_k_nodes(node: Node | None, k: int) -> bool:
    for _ in range(k):
        if node is None:
            return False
        node = node.next
    return True


def reverse_with_a_list(head: Node | None) -> Node | None:
    """The honest O(n)-space alternative. Say out loud that you are trading
    space for simplicity if you write this one."""
    values = to_values(head)
    return from_values(values[::-1])


if __name__ == "__main__":
    print(to_values(reverse(from_values([1, 2, 3, 4, 5]))))       # [5, 4, 3, 2, 1]
    print(to_values(reverse(from_values([1]))))                   # [1]
    print(to_values(reverse(from_values([]))))                    # []
    print(to_values(reverse(from_values([1, 2]))))                # [2, 1]

    print(to_values(reverse_recursive(from_values([1, 2, 3, 4]))))  # [4, 3, 2, 1]
    print(to_values(reverse_recursive(from_values([]))))            # []

    print(to_values(reverse_between(from_values([1, 2, 3, 4, 5]), 2, 4)))  # [1,4,3,2,5]
    print(to_values(reverse_between(from_values([1, 2, 3, 4, 5]), 1, 5)))  # [5,4,3,2,1]
    print(to_values(reverse_between(from_values([1, 2, 3]), 2, 2)))        # [1,2,3]
    print(to_values(reverse_between(from_values([5]), 1, 1)))              # [5]

    print(to_values(reverse_k_group(from_values([1, 2, 3, 4, 5]), 2)))   # [2,1,4,3,5]
    print(to_values(reverse_k_group(from_values([1, 2, 3, 4, 5]), 3)))   # [3,2,1,4,5]
    print(to_values(reverse_k_group(from_values([1, 2, 3, 4]), 4)))      # [4,3,2,1]
    print(to_values(reverse_k_group(from_values([1, 2, 3]), 5)))         # [1,2,3]

    # the recursion limit is real
    long_list = from_values(list(range(5000)))
    try:
        reverse_recursive(long_list)
    except RecursionError as error:
        print(f"RecursionError: {error}")
    print(to_values(reverse(from_values(list(range(5000)))))[:3])        # [4999, 4998, 4997]
```

---

## 6. What it costs

### The iterative version

```
 time:   the loop runs once per node          O(n)
         each iteration is 4 assignments      constant
 space:  previous, current, next_node          O(1)
```

Count the assignments out loud: `4n` writes for a list of `n` nodes, and no allocation at all. That is
about as cheap as an algorithm gets, and the O(1) space is the reason this is the version to write.

### The recursive version

```
 time:   O(n)   one call per node
 space:  O(n)   one stack frame per node — NOT O(1)
```

Python's default recursion limit is 1000, so:

```
RecursionError: maximum recursion depth exceeded
```

fires at about a thousand nodes. That is not a theoretical limit, it is a crash on any realistic
input, and it is the reason the iterative version is the right answer even when the interviewer asks
for both. Say it rather than waiting to be told — "recursive is O(n) stack and raises past a thousand
nodes in Python, so I would ship the iterative one."

### Reversing a sublist and reversing in groups

```
 reverse_between:  O(n) time, O(1) space
                   the walk to `left` is O(left), the reversal is O(right - left)
 reverse_k_group:  O(2n) time -> O(n), O(1) space
                   each node is visited once by the counting walk and once by the reversal
```

The `2n` is worth stating precisely rather than hiding: **each node is walked over twice, once to
check the group is full and once to reverse it.** Still linear, and the alternative — reverse first,
then undo if the group was short — costs the same in the bad case and is much harder to get right.

### Against the O(n)-space alternative

```
 values into a Python list, reverse, rebuild:
   time   O(n), three passes
   space  O(n) for the values list plus n new nodes
   nodes allocated: n
 in place:
   time   O(n), one pass
   space  O(1)
   nodes allocated: 0
```

At a million nodes that is roughly 48 MB of new nodes against three variables. The list version is not
*wrong*, and if you write it you should say what you traded — but no interviewer asking "reverse a
linked list" wants it.

---

## 7. The traps

### Trap 1 — overwriting `current.next` before saving it

```python
    while current is not None:
        current.next = previous        # WRONG ORDER — the rest of the list is gone
        next_node = current.next       # this is now `previous`, not the next node
```

The loop runs twice and stops. `reverse(from_values([1, 2, 3]))` returns `[1]`. No exception — the
list simply ends. This is Nalini's boy letting go before looking back, and it is the single defining
mistake of this problem.

### Trap 2 — returning `head`

```python
    return head                        # WRONG
```

After the loop, `head` refers to the old first node, which is now the **last** node and points at
`None`. So you return a one-element list. `previous` is the new head.

### Trap 3 — the missing `head.next = None` in the recursive version

```python
    new_head = reverse_recursive(head.next)
    head.next.next = head
    return new_head                    # forgot: head.next = None
```

The old head still points forward at the node that now points back at it. Printing the result:

```
KeyboardInterrupt
```

after the output list has grown until memory ran out. A two-node cycle, and the only symptom is that
nothing returns.

### Trap 4 — capturing the sublist's tail too late

```python
    before.next = previous
    tail_of_reversed = before.next     # WRONG — this is now the FIRST node
```

After the reversal, the node that used to be first is now last, and `before.next` points at what used
to be last. Capture it before you start, when it is still `before.next` and still first.

### Trap 5 — reversing a short final group

```python
    while group_before.next is not None:      # no k-count check
```

On `[1, 2, 3]` with k = 5, this reverses the three nodes it finds and returns `[3, 2, 1]`, when the
specification says a group of fewer than k is left alone. Check first, with a separate walk.

### Trap 6 — `RecursionError` treated as an edge case

```
RecursionError: maximum recursion depth exceeded
```

It is not an edge case. A list of a few thousand nodes is ordinary, and the recursive solution simply
does not work on it in Python. Raising `sys.setrecursionlimit` is not a fix — it moves the failure
from a clean exception to a segmentation fault when the C stack runs out.

### Trap 7 — reversing values instead of pointers

```python
    values = to_values(head)
    node, i = head, len(values) - 1
    while node is not None:
        node.value = values[i]         # copies values back in reverse
        ...
```

It produces the right output and it is O(n) space, and it is a different algorithm from the one you
were asked for. Worse, it is wrong the moment the nodes carry anything other than a value — an
identity, a reference held elsewhere, extra fields. The question is about pointers. Move the pointers.

### Trap 8 — `while current.next is not None`

```python
    while current.next is not None:    # stops one node early
```

The last node never gets its arrow turned, so it still points at `None` and ends up detached.
`reverse([1, 2, 3])` returns `[2, 1]`. The loop condition is `current is not None`, because the node
itself is what you are processing, not the link out of it.

---

## 8. In the interview

### How it gets asked

- The warm-up: *"Reverse a linked list."* LeetCode 206. Often the first five minutes of a longer
  round.
- Immediately after: *"Now do it recursively."* They want to see whether you can, and whether you will
  volunteer the stack cost.
- The escalation: *"Reverse only the nodes between positions m and n."* LeetCode 92.
- The hard one: *"Reverse the nodes in groups of k."* LeetCode 25, Hard, and it is this loop plus
  bookkeeping.
- The applied version: *"Check whether a linked list is a palindrome, in O(1) space."* — find the
  middle, reverse the second half, compare, and ideally restore.

### What to say out loud, in the first ninety seconds

1. **State what is actually changing.** "No node moves and nothing is allocated — I am turning each
   `next` pointer round exactly once, so this is O(n) time and O(1) space."
2. **Name the hazard before writing.** "The danger is that the moment I overwrite `current.next`, I
   lose my only reference to the rest of the list. So the first line of the loop saves it."
3. **Say the four lines as a phrase.** "Save the next node, turn the arrow round, move previous
   forward, move current forward — in that order."
4. **Say what `previous` starts as, and why.** "`previous` starts as `None`, which does two jobs: the
   old head correctly becomes the tail pointing at nothing, and it is the value I return for an empty
   list."
5. **Say the return.** "I return `previous`, not `head`. When the loop ends, `previous` is the old
   tail, which is the new head."
6. **Then offer the recursive version with its cost**, rather than waiting to be asked to compare.

### The follow-ups

**"Now do it recursively."**
"The base case is an empty list or a single node — both are already reversed. Otherwise I reverse
everything after `head` and trust that call to have done its job. Then `head.next` is still pointing
at what was the second node, which is now the last node of the reversed part, so I make it point back
at `head`, and I set `head.next = None` to make `head` the new tail. That last line is mandatory —
without it the two nodes point at each other and the list has a cycle. I return the new head
unchanged all the way up, because the new head is the old tail and it was found at the very bottom.
The cost is O(n) stack, and in Python it raises `RecursionError` past about a thousand nodes, so I
would ship the iterative version."

**"Reverse only positions m to n."**
"Walk to the node just before position m and hold it. Capture the node *at* position m as well,
before doing anything, because after the reversal it will be the last node of the section and there
is no way to find it again. Reverse exactly n − m + 1 nodes with the same four lines. Then two
reattachments: the node before points at the new first node of the section, and the captured node
points at whatever followed the section. I would use a dummy head, because if m is 1 the head itself
changes."

**"Reverse in groups of k, leaving a short final group alone."**
"Three parts. First, check there are k nodes remaining, with a separate walk — before touching
anything, so I never reverse a short group and then have to undo it. Second, reverse exactly k nodes.
Third, reattach: the node before the group points at the group's new first node, and the group's old
first node — which is now its last — points at whatever comes next. Then the node before the next
group is that old first node. It is O(2n), so still linear, and O(1) space."

**"Can you do it in O(1) space recursively?"**
"No. Recursion uses stack space proportional to the depth by definition, and the depth here is n.
Tail-call elimination would fix it in a language that does that, and Python deliberately does not.
So if the constraint is O(1) space, the answer is the iterative version."

**"Where would you actually need this?"**
"Two places. Checking whether a list is a palindrome in O(1) space: find the middle with fast and slow
pointers, reverse the second half, compare, and reverse it back so I do not leave the caller's data
mangled — leaving it reversed is a real bug and worth mentioning. And adding two numbers stored as
linked lists with the most significant digit first, where reversing both makes the carry propagate in
the natural direction."

**"Your loop condition — why `current` and not `current.next`?"**
"Because `current` is the node I am processing, not the link. With `current.next is not None` the loop
stops one node early, the last node never gets its arrow turned, and it ends up detached — reversing
`[1, 2, 3]` gives `[2, 1]`."

### A model answer

Asked: *reverse a linked list.*

> "Let me say what is actually changing first, because it decides the approach. No node moves,
> nothing is allocated, no value is copied — every node's `next` pointer is turned round exactly once.
> So this should be one pass, O(n) time and O(1) extra space.
>
> The hazard is a single line. The moment I overwrite `current.next`, I have destroyed my only way of
> reaching the rest of the list — nothing else points at it. So the first thing inside the loop is to
> save it.
>
> Three variables. `previous`, which starts as `None`. `current`, which starts at the head. And
> `next_node`, created inside the loop because it only has to survive one iteration. `previous`
> starting as `None` is doing two jobs, which is worth noticing: it makes the old head correctly
> become the new tail pointing at nothing, and it is the correct return value when the list is empty.
>
> The loop is four lines and the order is not negotiable. Save the next node. Turn this node's arrow
> round to point at `previous`. Move `previous` up to `current`. Move `current` up to the saved node.
> Save, turn, previous up, current up.
>
> When the loop ends, `current` is `None` and `previous` is the last node I visited — which is the old
> tail, and the old tail is the new head. So I return `previous`, not `head`. `head` now refers to the
> node that ended up last, so returning it hands back a one-element list, and there is no error to
> tell you.
>
> Complexity: four assignments per node, so 4n writes, one pass, and three references of extra space
> regardless of length. There is an O(n)-space version — read the values into an array, reverse it,
> rebuild — and I would only write that if simplicity mattered more than space, and I would say so
> rather than let it pass as the intended answer.
>
> If you want it recursively: the base case is an empty list or a single node. Otherwise reverse
> everything after `head`, and then, standing on `head`, note that `head.next` still points at what was
> the second node, which is now the *last* node of the reversed part. So `head.next.next = head` makes
> it point back at me, and `head.next = None` makes me the new tail. That second line is mandatory —
> leave it out and those two nodes point at each other and printing the list never returns. The
> recursive version is O(n) stack and raises `RecursionError` past about a thousand nodes in Python, so
> I would ship the iterative one and mention the recursive one as the shape that generalises to
> trees."

---

## 9. Recall card

- **Nothing moves and nothing is allocated — you turn each `next` round exactly once.** Three
  variables, four lines, one fixed order: **save the next node · turn the arrow · previous up ·
  current up.** *Look behind you, let go, take hold.*
- **Line 1 is the whole problem.** `current.next` is overwritten on line 2, so failing to save it
  first loses the entire rest of the list — no exception, `[1,2,3]` just returns `[1]`.
- **Return `previous`, not `head`.** At the end, `current is None` and `previous` is the old tail,
  which is the new head; `head` now refers to the last node, so returning it gives a one-element
  list. And loop on `while current is not None`, never `current.next` — that stops one node early and
  detaches the tail.
- **Recursive: trust the call, then `head.next.next = head` and `head.next = None`.** The second line
  is **mandatory** — without it you build a two-node cycle and printing never returns. It is **O(n)
  stack**, and `RecursionError: maximum recursion depth exceeded` fires at about **1000** nodes in
  Python, so ship the iterative one.
- **The two escalations are this loop plus bookkeeping.** *Sublist* (LeetCode 92): use a **dummy**,
  and **capture the node at position `left` before reversing** — afterwards it is the last node and
  unfindable; then two reattachments. *Groups of k* (LeetCode 25): **count k nodes first**, before
  touching anything, so a short final group is never reversed and undone; O(2n) → O(n), O(1) space.
