---
day: 82
track: dsa
title: "Finding the middle, and the runner technique"
phase: "Linked lists"
status: written
---

# Day 082 · DSA — Finding the middle, and the runner technique

**After today you can:** You can find the middle and the Nth from the end in a single pass.

**The interviewer asks it as:** *Remove the Nth node from the end in one pass.*

---

## 1. What this is, and why they ask it

A linked list does not know its own length, and you cannot jump to position `n/2`. So the obvious way
to find the middle is to walk the whole list counting, then walk again to the halfway point. Two
passes, and correct.

The **runner technique** does it in one. You send two pointers along the list at once. Either one
moves twice as fast as the other — so when the fast one reaches the end, the slow one is at the middle
— or they move at the same speed with a **fixed gap** between them, so when the front one reaches the
end, the back one is exactly that many nodes from it.

Those two variants — different **speeds**, or a different **starting point** — solve a surprising
number of problems: the middle, the Nth from the end, whether the list is a palindrome, splitting the
list in half for a merge sort, and tomorrow's cycle detection. They ask it because the two-pass
solution is obvious and correct, so the question is really *"can you see the one-pass version, and can
you get the off-by-one right?"* — and the off-by-one is genuinely fiddly. `while fast and fast.next`
and `while fast.next and fast.next.next` differ by one character group and give you different middles.

---

## 2. The story

The school is putting up a compound wall along the back of the field and Krishnappa has the job of
painting it.

It is a long wall. It runs from the corner by the water tank, past the field, and curves out of sight
behind the trees, and you cannot see one end from the other. Nobody has ever measured it and the tape
in the storeroom is thirty metres.

He needs two marks on it before he starts.

The first is the exact middle, because the school wants a gate there and the gate has to be centred or
it will look wrong for the next forty years.

The second is a point exactly twenty paces in from the far end, where a board is going up.

His nephew Shivu suggested walking it once to count the paces, then walking it again to the halfway
number. Krishnappa did that once, years ago, on a different wall. It is an hour, and by the second
walk you have stopped trusting your own count.

What he does instead takes one walk.

For the middle, the two of them start together at the water-tank corner. Krishnappa walks normally.
Shivu takes two paces for every one of his uncle's — he has done it since he was small and it annoys
his uncle for the first hundred metres and then stops mattering. They keep together, one pace to two,
all the way. When Shivu reaches the far corner, Krishnappa stops where he is and puts a chalk mark on
the stone at his shoulder. That is the middle. He does not know how long the wall is and he does not
need to.

For the second mark it is a different trick, and Shivu likes this one better. They both walk at the
same speed, but they do not start together. Shivu goes twenty paces ahead first and waits. Then they
walk in step, keeping exactly that gap, neither closing it nor opening it. When Shivu reaches the far
corner, Krishnappa stops. He is twenty paces from the end, exactly, and again neither of them knows
how long the wall is.

The one thing that goes wrong, and it went wrong on the wall behind the market, is when the wall is
shorter than the gap. Shivu walks his twenty paces and finds he is already past the end, and there is
nothing to measure from. Krishnappa says you have to check that first, before either of you starts
walking.

---

## 3. The idea in plain English

Two walkers, one wall, one pass. **Different speeds** finds the middle. A **fixed gap** finds a point
a known distance from the end. Neither needs to know the length.

### The speed variant: finding the middle

```python
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next            # one step
        fast = fast.next.next       # two steps
    return slow                     # slow is at the middle
```

Why it works: `fast` covers exactly twice the distance of `slow` at every moment. When `fast` has
travelled `n` steps and stopped, `slow` has travelled `n/2`. That is the whole argument, and it is one
sentence.

The loop condition is doing two jobs. `fast is not None` protects against an even-length list where
`fast` lands exactly on `None`. `fast.next is not None` protects against an odd-length list where
`fast` lands on the last node and `fast.next.next` would explode. **Both checks are required, and
`fast is not None` must come first**, because `and` short-circuits.

### The even-length ambiguity, which you must raise

A list of four nodes has **two** middles. `[1, 2, 3, 4]` — is the middle 2 or 3?

```
 while fast and fast.next:              -> slow ends on 3   (the SECOND middle)
 while fast.next and fast.next.next:    -> slow ends on 2   (the FIRST middle)
```

Both are one line. Which you want depends on the problem:

- **Splitting for a merge sort** wants the *first* middle, so that `[1,2]` and `[3,4]` are equal
  halves and the recursion always shrinks.
- **"Return the middle node"** (LeetCode 876) wants the *second* middle, because that is what the
  problem statement says.
- **Palindrome checking** wants the second middle, so the second half is the shorter or equal one.

**Ask which one before writing.** An interviewer who has to tell you there are two middles has learned
something; one who hears you ask has learned something better.

### The gap variant: the Nth from the end

```python
    fast = head
    for _ in range(n):              # open the gap FIRST
        fast = fast.next
    slow = head
    while fast is not None:         # now walk in step
        fast = fast.next
        slow = slow.next
    return slow                     # slow is the nth node from the end
```

Shivu walking his twenty paces before either of them starts. The gap never changes after that, so when
`fast` falls off the end, `slow` is exactly `n` nodes behind it.

And Krishnappa's warning is the edge case: **if the list is shorter than `n`, the opening walk runs
off the end.**

```
AttributeError: 'NoneType' object has no attribute 'next'
```

Check inside the opening loop, and decide what to do — raise, or return the head unchanged — and say
which you chose.

### Removing the Nth from the end, and why the dummy comes back

To *remove* a node you need the node **before** it, from [day 079](../day-079-list-traversal/README.md).
So `slow` must stop one node earlier than it does above. Two ways to arrange that, and the good one is
the dummy head from [day 080](../day-080-dummy-head/README.md):

```python
    dummy = Node(0, head)
    fast = slow = dummy             # both start at the dummy
    for _ in range(n):
        fast = fast.next
    while fast.next is not None:    # stop when fast is ON the last node
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return dummy.next
```

The dummy does two jobs at once here, and it is worth pointing at both. It shifts `slow` back by one
so it lands on the **predecessor** of the target. And it makes "remove the first node" — `n` equal to
the length — an ordinary case instead of a special one.

Without the dummy you need a gap of `n + 1` and a separate check for whether the head is the target.
That works and it is harder to get right under pressure.

### The other things the runner technique gives you

**Split the list in half**, which is the first step of a merge sort on a linked list
([day 084](../day-084-merging-and-sorting-lists/README.md)). Find the *first* middle, then cut:
`second = middle.next; middle.next = None`. Forgetting to cut is the bug — you get two lists that
share a tail, and the recursion never terminates.

**Palindrome in O(1) space** (LeetCode 234). Find the middle, reverse the second half with
[day 081](../day-081-reversing-a-list/README.md)'s four lines, walk both halves comparing, then
reverse the second half back so you do not hand the caller a mangled list.

**Reorder the list** (LeetCode 143): `1→2→3→4→5` becomes `1→5→2→4→3`. Split, reverse the second half,
interleave. Three techniques from three days, in one function.

**Cycle detection**, which is tomorrow. If the list loops, `fast` never reaches the end — and it
eventually laps `slow`. Same two pointers, entirely different conclusion.

### The honest comparison with two passes

The two-pass version is: count the nodes, then walk `length // 2`. It is O(n) time and O(1) space —
**the same complexity as the one-pass version.** So the runner technique is not asymptotically better;
it is one pass instead of two, which halves the constant.

Say that plainly rather than overclaiming. The reasons to prefer it are that it works on a stream you
can only read once, and that the interviewer asked for one pass. If neither applies, counting is
easier to read and easier to get right, and there is no shame in saying so.

---

## 4. The picture

Finding the middle of `[1, 2, 3, 4, 5]`. `s` is slow, `f` is fast.

```
 start        [1] [2] [3] [4] [5] None
              s,f

 step 1       [1] [2] [3] [4] [5] None
                  s       f

 step 2       [1] [2] [3] [4] [5] None
                      s       f

 fast.next is None -> stop.  slow is on 3, the middle of five.  Correct.
```

And on an even length, `[1, 2, 3, 4]`, where the two conditions part company:

```
 while fast and fast.next:
   start   s,f at [1]
   step 1  s=[2]  f=[3]
   step 2  s=[3]  f=None      -> stop.  slow = 3   (SECOND middle)

 while fast.next and fast.next.next:
   start   s,f at [1]
   step 1  s=[2]  f=[3]
                              -> fast.next is [4], fast.next.next is None: stop
                                 slow = 2          (FIRST middle)
```

What to notice: **the same walk, two different stopping rules, two different answers.** Neither is
wrong. The problem statement decides.

The gap variant, removing the 2nd from the end of `[1, 2, 3, 4, 5]`:

```
 dummy -> [1] [2] [3] [4] [5] None
 s,f
          open a gap of n = 2

 dummy -> [1] [2] [3] [4] [5] None
   s              f

          now walk together until f is ON the last node

 dummy -> [1] [2] [3] [4] [5] None
                   s       f          <- f.next is None: stop

 slow is on [3], which is the node BEFORE the target [4].
 slow.next = slow.next.next   ->  [1] [2] [3] [5]
```

What to notice: `slow` started at the **dummy**, not at the head. That one decision is what puts it on
the predecessor instead of on the target, and it is why `n` equal to the list length — removing the
head — needs no special case.

---

## 5. The code, built step by step

### Step 1 — the middle, with the condition explained

```python
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
```

Two guards, and both are needed. On an even-length list `fast` lands on `None`; on an odd-length list
it lands on the last node and `fast.next.next` would raise. `fast is not None` must be first, because
`and` short-circuits and the second check dereferences.

### Step 2 — the other middle, one line different

```python
    slow = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next
```

Now the checks look one node further ahead, so the walk stops one step earlier and `slow` lands on the
first middle. Requires `head` to be non-`None`, so guard the empty list separately.

### Step 3 — the gap, with the length check

```python
    fast = head
    for _ in range(n):
        if fast is None:
            raise ValueError(f"list has fewer than {n} nodes")
        fast = fast.next
```

Krishnappa's warning, in code. Check *inside* the loop, before dereferencing.

### Step 4 — walking in step

```python
    slow = head
    while fast is not None:
        fast = fast.next
        slow = slow.next
```

The gap is fixed the moment the first loop ends and nothing changes it. When `fast` becomes `None`,
`slow` is `n` nodes from the end.

### Step 5 — splitting, and the cut that people forget

```python
    middle = first_middle(head)
    second = middle.next
    middle.next = None              # THE CUT. Without it, the halves share a tail.
    return head, second
```

One line, and leaving it out gives you two lists that are really one list, so a merge sort recurses
for ever. Write the cut immediately after finding the middle, in the same breath.

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


def middle_second(head: Node | None) -> Node | None:
    """The SECOND middle on an even-length list. [1,2,3,4] -> 3.
    This is what LeetCode 876 asks for. O(n) time, O(1) space."""
    slow = fast = head
    while fast is not None and fast.next is not None:   # order matters: `and` short-circuits
        slow = slow.next
        fast = fast.next.next
    return slow


def middle_first(head: Node | None) -> Node | None:
    """The FIRST middle on an even-length list. [1,2,3,4] -> 2.
    This is the one a merge sort needs, so both halves shrink."""
    if head is None:
        return None
    slow = fast = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow


def nth_from_end(head: Node | None, n: int) -> Node:
    """The nth node counting from the end (n = 1 is the last node).

    Open a gap of n, then walk both in step. When `fast` falls off the end,
    `slow` is exactly n nodes behind it.
    """
    if n < 1:
        raise ValueError("n must be at least 1")

    fast = head
    for _ in range(n):
        if fast is None:
            raise ValueError(f"list has fewer than {n} nodes")
        fast = fast.next

    slow = head
    while fast is not None:
        fast = fast.next
        slow = slow.next
    return slow


def remove_nth_from_end(head: Node | None, n: int) -> Node | None:
    """Remove the nth node from the end, in one pass.

    The dummy does two jobs: it shifts `slow` back one so it lands on the
    PREDECESSOR of the target, and it makes removing the head an ordinary case.
    """
    dummy = Node(0, head)
    fast = slow = dummy

    for _ in range(n):
        if fast.next is None:
            raise ValueError(f"list has fewer than {n} nodes")
        fast = fast.next

    while fast.next is not None:        # stop with fast ON the last node
        fast = fast.next
        slow = slow.next

    slow.next = slow.next.next
    return dummy.next


def split_in_half(head: Node | None) -> tuple[Node | None, Node | None]:
    """Cut the list into two halves at the FIRST middle.

    The cut is mandatory: without `middle.next = None` the two halves share a
    tail, and a merge sort built on this never terminates.
    """
    if head is None or head.next is None:
        return head, None
    middle = middle_first(head)
    second = middle.next
    middle.next = None                  # THE CUT
    return head, second


def reverse(head: Node | None) -> Node | None:
    """Day 081's four lines, needed by the two functions below."""
    previous, current = None, head
    while current is not None:
        next_node = current.next
        current.next = previous
        previous = current
        current = next_node
    return previous


def is_palindrome(head: Node | None) -> bool:
    """O(n) time, O(1) space: find the middle, reverse the second half,
    compare, then put the list back the way you found it.

    Restoring matters — leaving the caller's list half-reversed is a real bug
    even though the tests pass without it.
    """
    if head is None or head.next is None:
        return True

    middle = middle_first(head)
    second = reverse(middle.next)
    middle.next = None

    left, right = head, second
    answer = True
    while right is not None:            # the second half is the shorter one
        if left.value != right.value:
            answer = False
            break
        left, right = left.next, right.next

    middle.next = reverse(second)       # restore
    return answer


def reorder(head: Node | None) -> Node | None:
    """[1,2,3,4,5] -> [1,5,2,4,3]. Split, reverse the second half, interleave.
    Three techniques from three days in one function."""
    if head is None or head.next is None:
        return head

    first, second = split_in_half(head)
    second = reverse(second)

    a, b = first, second
    while b is not None:
        a_next, b_next = a.next, b.next
        a.next = b
        b.next = a_next if a_next is not None else b_next
        a, b = a_next, b_next
    return first


if __name__ == "__main__":
    print(middle_second(from_values([1, 2, 3, 4, 5])).value)      # 3
    print(middle_second(from_values([1, 2, 3, 4])).value)         # 3   (second)
    print(middle_first(from_values([1, 2, 3, 4])).value)          # 2   (first)
    print(middle_second(from_values([1])).value)                  # 1
    print(middle_second(from_values([])))                         # None

    print(nth_from_end(from_values([1, 2, 3, 4, 5]), 1).value)    # 5
    print(nth_from_end(from_values([1, 2, 3, 4, 5]), 5).value)    # 1
    try:
        nth_from_end(from_values([1, 2]), 3)
    except ValueError as error:
        print(f"ValueError: {error}")     # list has fewer than 3 nodes

    print(to_values(remove_nth_from_end(from_values([1, 2, 3, 4, 5]), 2)))  # [1,2,3,5]
    print(to_values(remove_nth_from_end(from_values([1, 2, 3, 4, 5]), 5)))  # [2,3,4,5]
    print(to_values(remove_nth_from_end(from_values([7]), 1)))              # []

    left, right = split_in_half(from_values([1, 2, 3, 4, 5]))
    print(to_values(left), to_values(right))                      # [1, 2, 3] [4, 5]
    left, right = split_in_half(from_values([1, 2, 3, 4]))
    print(to_values(left), to_values(right))                      # [1, 2] [3, 4]

    for values in ([1, 2, 2, 1], [1, 2, 3, 2, 1], [1, 2], [1], []):
        original = from_values(values)
        result = is_palindrome(original)
        print(values, result, to_values(original))    # list must be UNCHANGED

    print(to_values(reorder(from_values([1, 2, 3, 4, 5]))))       # [1, 5, 2, 4, 3]
    print(to_values(reorder(from_values([1, 2, 3, 4]))))          # [1, 4, 2, 3]
```

The palindrome loop printing the original list afterwards is the test that matters. A version that
forgets to restore still returns the right boolean, and hands the caller a list that has been cut in
half and reversed.

---

## 6. What it costs

### Time and space

```
 middle              O(n) time, O(1) space   — one pass, two references
 nth_from_end        O(n) time, O(1) space
 remove_nth_from_end O(n) time, O(1) space
 split_in_half       O(n) time, O(1) space
 is_palindrome       O(n) time, O(1) space   — three walks, still linear
 reorder             O(n) time, O(1) space
```

Count the middle out loud: `slow` takes `n/2` steps and `fast` takes `n/2` iterations of two steps
each, so about `1.5n` pointer moves in one pass. The two-pass version is `n` moves to count plus `n/2`
to walk, which is the same `1.5n` — **so the runner technique is not doing less work, it is doing it
in one traversal instead of two.**

That distinction matters when the data can only be read once, and it matters much less otherwise. Say
it honestly.

### Against the alternatives

```
 middle, two passes:      count n, then walk n/2      O(n) time, O(1) space
 middle, runner:          one pass                    O(n) time, O(1) space
 middle, into a list:     copy all values, index n/2  O(n) time, O(n) SPACE
```

The array version is the one to reject explicitly: at a million nodes it allocates a
million-element list — about 8 MB of pointers plus the values — to answer a question that needs two
variables.

### Palindrome, three ways

```
 copy values into a list and compare with its reverse:  O(n) time, O(n) space
 use a stack of the first half:                         O(n) time, O(n/2) space
 runner + reverse in place:                             O(n) time, O(1) space
```

The last one is what the follow-up asks for, and it is the reason today and yesterday are next to each
other in the syllabus.

### The `1.5n` versus `2n` question, which does get asked

For `remove_nth_from_end`, the two-pass version walks `n` to count and then `n − k` to reach the
predecessor — about `2n` pointer moves. The one-pass version walks `n` with `fast` and `n − k` with
`slow`, which is also about `2n` moves, but in a **single traversal**.

So the honest answer to "is one pass faster?" is: **the same number of pointer moves, half the number
of traversals.** On a linked list where each node is a fresh cache miss, one traversal is genuinely
better than two — but it is a constant factor, not a complexity difference, and claiming otherwise
will get you corrected.

---

## 7. The traps

### Trap 1 — the loop condition, in the wrong order

```python
    while fast.next is not None and fast is not None:      # WRONG ORDER
```

```
AttributeError: 'NoneType' object has no attribute 'next'
```

`and` evaluates left to right, so `fast.next` is dereferenced before `fast` is checked. Fires on any
even-length list. **`fast is not None` first, always.**

### Trap 2 — the wrong middle

```python
    while fast is not None and fast.next is not None:      # gives the SECOND middle
```

used where the first middle was wanted. In a merge sort this is fatal rather than merely wrong: on a
two-element list `[1, 2]`, the second middle is node 2, so the split gives `[1, 2]` and `[]`, the
recursion does not shrink, and you get:

```
RecursionError: maximum recursion depth exceeded
```

**For splitting, always the first middle.** Say which one you are using and why, every time.

### Trap 3 — forgetting the cut

```python
    middle = middle_first(head)
    second = middle.next
    return head, second                    # forgot: middle.next = None
```

Both "halves" still share every node from the middle onwards. `to_values(left)` prints the whole list.
A merge sort built on this recurses on inputs that never get smaller. No error until the recursion
limit.

### Trap 4 — the gap running off a short list

```python
    for _ in range(n):
        fast = fast.next                   # no check
```

```
AttributeError: 'NoneType' object has no attribute 'next'
```

when `n` exceeds the length. Check inside the loop and decide the behaviour — raise, or treat it as
"remove nothing" — and say which. Interviewers ask "what if n is bigger than the list?" precisely
because the naive code crashes.

### Trap 5 — `slow` starting at the head when you need the predecessor

```python
    fast = head
    for _ in range(n): fast = fast.next
    slow = head
    while fast is not None:
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next             # slow is ON the target, not before it
```

This removes the node *after* the one you wanted. Start both at a dummy and stop when `fast.next` is
`None`, which puts `slow` on the predecessor and handles the head case for free.

### Trap 6 — not restoring the list in the palindrome solution

```python
    middle.next = None
    second = reverse(middle.next)
    ...
    return answer                          # list left cut in half and reversed
```

The function returns the correct boolean. It also hands back a mutated list, and the caller has no
idea. Every test that only checks the return value passes. **A read-only question must leave the data
as it found it**, and saying that unprompted is worth more than the algorithm.

### Trap 7 — assuming one pass is asymptotically better

It is not. Both are O(n) time and O(1) space, and both do about the same number of pointer moves. One
pass is better because it works on read-once data and because it touches memory once instead of twice.
Overclaiming here is an easy way to be corrected in an interview.

### Trap 8 — the empty list and the single node

`middle_first` dereferences `head.next` in its loop condition, so `head is None` must be handled
before it. `[1]` is its own middle and its own palindrome. `remove_nth_from_end(from_values([7]), 1)`
must return an empty list, not raise. Run all three before you say you are done.

---

## 8. In the interview

### How it gets asked

- The base: *"Find the middle node of a linked list."* LeetCode 876. Almost always followed by "in one
  pass".
- The main event: *"Remove the Nth node from the end of the list, in one pass."* LeetCode 19.
- The application: *"Is this linked list a palindrome? Now do it in O(1) space."* LeetCode 234.
- The composite: *"Reorder the list so it goes first, last, second, second-last…"* LeetCode 143 —
  three techniques in one problem.
- Tomorrow's version: *"Does this list have a cycle?"* Same two pointers, different question.

### What to say out loud, in the first ninety seconds

1. **State the two-pass version and why you are not writing it.** "I could count the nodes and then
   walk halfway. That is O(n) and correct. You asked for one pass, so I will use two pointers."
2. **Name which variant you need.** "Two pointers at different speeds finds the middle. Two pointers
   at the same speed with a fixed gap finds a fixed distance from the end. This problem is the second
   one."
3. **Say the invariant in one sentence.** "I open a gap of `n` first, then move both together, so the
   gap never changes — when the front pointer falls off the end, the back one is exactly `n` nodes
   from it."
4. **Raise the ambiguity yourself, if it is the middle.** "On an even-length list there are two
   middles. Which do you want? For splitting I would take the first, so both halves shrink."
5. **Name the edge case before writing.** "If `n` is bigger than the list, the opening walk runs off
   the end, so I check inside that loop."
6. **If removing, say why the dummy.** "I need the node *before* the target, so both pointers start at
   a dummy — that also makes removing the head an ordinary case."

### The follow-ups

**"What if the list has an even number of nodes?"**
"Then there are two middles, and the loop condition decides which you get. `while fast and fast.next`
lands on the second; `while fast.next and fast.next.next` lands on the first. Neither is more correct
— it depends what you are doing. If I am splitting for a merge sort I need the first, because with the
second, a two-element list splits into itself and an empty list and the recursion never shrinks."

**"What if n is larger than the length of the list?"**
"The opening walk runs off the end and you get `AttributeError: 'NoneType' object has no attribute
'next'`. So I check inside that loop. What to do then is a product decision I would ask about: raise,
or treat it as 'remove nothing' and return the list unchanged. LeetCode guarantees `n` is valid, but
real code does not."

**"Why does `slow` start at the dummy rather than the head?"**
"Because I need the node *before* the one being removed, and starting `slow` one node earlier is the
cheapest way to get it — the alternative is a gap of `n + 1`, which is easy to get wrong. The dummy
also means that removing the head, when `n` equals the length, needs no special case at all."

**"Is one pass actually faster than two?"**
"Not asymptotically — both are O(n) time and O(1) space, and both do roughly the same number of
pointer moves. What one pass buys is a single traversal instead of two, which matters when each node
is a separate cache miss, and it is required if the data can only be read once, like a stream. I would
not claim a complexity improvement, because there is not one."

**"Now check whether the list is a palindrome in O(1) space."**
"Three steps, all from this week. Find the first middle with the runner. Reverse the second half in
place with the three-pointer loop. Walk the two halves comparing values, stopping when the second half
runs out, since it is the shorter one on an odd length. Then reverse the second half back and
reattach, because leaving the caller's list cut in half and reversed is a real bug even though the
boolean is right."

**"Where else does this technique turn up?"**
"Splitting a list for a merge sort, which is the first half of merge sort on linked lists. Reordering
a list into first-last-second-second-last, which is split, reverse, interleave. And cycle detection,
where the fast pointer never reaches the end and instead laps the slow one — same two pointers,
completely different conclusion."

### A model answer

Asked: *remove the Nth node from the end of the list, in one pass.*

> "The two-pass version is: walk the list counting to get the length, then walk again to position
> length minus n. That is O(n) and perfectly correct, and I mention it because it is the baseline you
> are asking me to beat.
>
> The one-pass version uses two pointers with a **fixed gap**. I move one pointer forward `n` steps
> first, so the two are exactly `n` apart. Then I move both together, one step each, so the gap never
> changes. When the front pointer falls off the end, the back one is exactly `n` nodes from the end —
> and I never had to know the length.
>
> Two adjustments turn 'find it' into 'remove it'.
>
> First, to remove a node I need the node *before* it, because I cannot reach backwards. So the back
> pointer has to stop one node earlier. I do that by starting both pointers at a dummy node placed in
> front of the head, rather than at the head itself.
>
> Second, that same dummy handles the case where `n` equals the length — removing the head. Without
> it, that is a special case with its own branch, and the alternative arrangement is a gap of `n + 1`,
> which is one of those off-by-ones that is very easy to get wrong when someone is watching.
>
> The edge case I would check before writing the loop: if `n` is larger than the list, the opening
> walk dereferences `None` and you get an `AttributeError`. So the check goes inside that first loop.
> Whether to raise or to return the list unchanged is a decision I would ask you about.
>
> Then the second loop walks both pointers until the fast one is *on* the last node — not past it —
> which leaves the slow one on the predecessor of the target. One assignment removes the node, and I
> return `dummy.next` rather than `head`, because the head may be the node I just removed.
>
> Complexity: O(n) time, O(1) space, one traversal. I would not claim it is asymptotically faster than
> counting first — both are linear and both do about the same number of pointer moves. What it buys is
> one pass over memory instead of two, which matters on a linked list where every node is a separate
> cache miss, and it is the only option if the data can be read only once.
>
> Before I say I am done: I would run it on a single-node list with n equal to one, which must return
> an empty list; on n equal to the length, which removes the head; and on n equal to one, which removes
> the tail."

---

## 9. Recall card

- **Two variants of one idea, and naming which you need is the first move.** Different **speeds**
  (`slow += 1`, `fast += 2`) finds the **middle**; a fixed **gap** (`fast` starts `n` ahead, then both
  move together) finds a **fixed distance from the end**. Neither needs the length.
- **The middle's loop condition is doing two jobs and the order matters:**
  `while fast is not None and fast.next is not None` — the first guard protects even lengths, the
  second odd, and `and` short-circuits so the null check must come first.
- **On an even length there are TWO middles — ask which.** `while fast and fast.next` → the **second**
  (LeetCode 876). `while fast.next and fast.next.next` → the **first**, which is what **splitting for a
  merge sort** needs: with the second, `[1,2]` splits into itself and nothing and you get
  `RecursionError`. And **the cut is mandatory** — `middle.next = None`, or the halves share a tail.
- **To *remove* the Nth from the end, start BOTH pointers at a dummy** — it lands `slow` on the
  **predecessor** and makes removing the head an ordinary case. Guard the opening walk, or a short
  list gives `AttributeError: 'NoneType' object has no attribute 'next'`.
- **One pass is not asymptotically better — both are O(n) time and O(1) space and do about the same
  pointer moves.** What it buys is **one traversal instead of two** (and read-once data). Applications:
  **palindrome in O(1) space** (middle → reverse → compare → **reverse back**, because a read-only
  question must leave the data as it found it) · **reorder** (split, reverse, interleave) · and
  tomorrow, **cycle detection** — the same two pointers, a completely different conclusion.
