---
day: 80
track: dsa
title: "The dummy head trick"
phase: "Linked lists"
status: written
---

# Day 080 · DSA — The dummy head trick

**After today you can:** You stop writing a special case for the head, in every linked list problem.

**The interviewer asks it as:** *Remove all nodes with a given value, including at the head.*

---

## 1. What this is, and why they ask it

Yesterday every operation had a special case for position zero, because the first node has no
predecessor and you cannot unlink a node without one. Today you delete that special case for ever,
with one line:

```python
    dummy = Node(0, head)
```

You put a fake node in front of the list. Now the real first node *has* a predecessor — the fake one —
so it is an ordinary node like every other, and the loop that handles the middle handles the front
too. At the end you return `dummy.next`, which is whatever the first node turned out to be.

They ask it because it turns a fifteen-line function with three branches into an eight-line function
with none, and because the interviewer can see immediately whether you have written linked-list code
before. "Remove all elements equal to `val`" is LeetCode 203 and it is the purest test there is: the
input `[7, 7, 7, 1, 7]` breaks every solution that treats the head with an `if` instead of a loop.
The same trick then reappears in merge-two-sorted-lists, partition, remove-duplicates, and
remove-Nth-from-end — half the problems in this phase.

---

## 2. The story

The lunch queue at Amina's school forms at twelve twenty, outside the hall, along the wall with the
handwash taps.

The rule the children are given on their first day is one sentence: **stand behind the person in front
of you, and move when they move.** It works. Nobody has to be told anything else. Forty children,
one rule.

Except for the child at the front, for whom the rule means nothing. There is nobody in front of them.
So the front child gets a different rule — watch the hall door, and when Sister opens it, go — and
because it is a different rule, it goes wrong in exactly the ways different rules go wrong. The front
child goes when the door opens for someone else. The front child does not notice the door at all
because he is talking. Two children argue about who is actually the front child. And when the front
child leaves, somebody has to work out who has become the front child now and tell them, which means
somebody has to be watching for that.

Sister Mary fixed it four years ago and it took her about a minute.

She stands at the front of the queue. She is not in the queue — she is not getting any lunch, she is
not counted, she does not move up — she just stands there, at the head, every day, so that there is
always somebody in front of the first child.

Now there is one rule and it is the same rule for everybody, including the child at the front. Stand
behind the person in front of you. Move when they move. The front child watches Sister's back like
everybody else watches the back in front of them. Nobody needs to be told they have become the front
child, because being the front child stopped being a special job.

There is one thing the teachers have to remember, and a student teacher got it wrong last term. When
you count the queue, you do not count Sister. She is standing in the line and she is not in the line.
The student teacher reported forty-one children waiting for thirty-nine lunches and there was a
short, unnecessary panic in the kitchen.

---

## 3. The idea in plain English

Sister Mary is a **dummy node** — sometimes called a sentinel head. She sits in front of the real
list, holds nothing anybody wants, and exists for one reason: **so that the first real node has a
predecessor.**

### The line, and what it removes

```python
    dummy = Node(0, head)
```

That is it. The `0` is never read; the value does not matter and by convention people write `0`. What
matters is `dummy.next = head`, because now:

- the first real node is reachable as `dummy.next`, exactly the way the third node is reachable as
  `something.next`;
- deleting the first node is `dummy.next = dummy.next.next`, which is the *same line* as deleting any
  other node;
- and the answer at the end is `dummy.next`, which correctly reflects whatever the first node became —
  including `None` if you deleted everything.

**`return dummy.next`, not `return head`.** This is the student teacher counting Sister. `head` still
refers to the node it always referred to, which may have been deleted, so returning it returns a
deleted node or a list with the removed element still at the front. It is the single most common bug
in this technique and it produces no error at all.

### The problem it is for

*Remove every node whose value is `7` from `[7, 7, 7, 1, 7]`.*

Without a dummy, the head needs a **loop**, not an `if`, because several leading nodes may match:

```python
    while head is not None and head.value == 7:      # a loop, not an if
        head = head.next
    if head is None:
        return None
    previous = head
    while previous.next is not None:
        if previous.next.value == 7:
            previous.next = previous.next.next
        else:
            previous = previous.next
    return head
```

Eleven lines, two loops, one `if`, and the top three lines exist purely because the head is special.
Now with a dummy:

```python
    dummy = Node(0, head)
    previous = dummy
    while previous.next is not None:
        if previous.next.value == 7:
            previous.next = previous.next.next
        else:
            previous = previous.next
    return dummy.next
```

Six lines, one loop, and the head is handled by the same code as everything else. The special case did
not get shorter — it stopped existing.

### The second rule, which is not about the dummy at all

Look at the `else` in that loop.

```python
        if previous.next.value == 7:
            previous.next = previous.next.next        # do NOT advance
        else:
            previous = previous.next                  # only advance when you keep
```

After a deletion, `previous.next` is a **new** node that you have not looked at yet. Advancing would
skip it, so two consecutive 7s would leave one behind. On `[1, 7, 7, 2]` an unconditional advance
returns `[1, 7, 2]`.

**Advance only when you keep.** Say it as you write it — it is the second half of this problem and it
has nothing to do with the dummy node.

### The other use: a dummy as a builder

The dummy has a second job that is just as common, and it looks different enough that people miss the
connection.

When you are **building** a new list — merging two sorted lists, partitioning, copying — the first
node is special again, for the mirror reason: you have nowhere to attach it to. So the code fills up
with "is this the first one?".

```python
    dummy = Node(0)          # holds nothing; exists so `tail` has somewhere to start
    tail = dummy
    while ...:
        tail.next = chosen_node
        tail = tail.next
    return dummy.next
```

`tail` is a moving cursor that always points at the last node built so far, and `dummy` is where it
starts. There is no "first node" case, because the first node is attached exactly like the fortieth.

Two uses, one idea: **a node that holds nothing, so that "the first one" stops being different.**

### Where it shows up

- **Remove Linked List Elements** (LeetCode 203) — the pure case.
- **Merge Two Sorted Lists** (21) — the builder form.
- **Remove Nth Node From End of List** (19) — where the node to remove may be the head, and the dummy
  also makes the two-pointer gap arithmetic come out right.
- **Remove Duplicates from Sorted List II** (82) — delete *all* copies, so even the head may be part
  of a run.
- **Partition List** (86) — two dummies, one per output list, then join them.
- **Reverse Nodes in k-Group** (25) — the hardest of them, and unwritable without a dummy.
- **Swap Nodes in Pairs** (24), **Add Two Numbers** (2), **Odd Even Linked List** (328).

If a problem can change the first node, use a dummy. That is the whole recognition rule.

### What it costs

One node — about 48 bytes — and one line. It does not change the complexity of anything. It is the
cheapest simplification in this course, and the reason to know it is that the branches it removes are
where the bugs are.

---

## 4. The picture

Removing every 7 from `[7, 7, 7, 1, 7]`.

```
 WITHOUT a dummy — the head needs its own loop first

  head
   |
   v
  [7]-->[7]-->[7]-->[1]-->[7]--> None
   ^^^^^^^^^^^^^^^^
   handled by loop 1        handled by loop 2
   (three iterations)


 WITH a dummy — one loop, and `previous` starts on a node that is not in the list

  dummy (not part of the list, value never read)
   |
   v
  [0]-->[7]-->[7]-->[7]-->[1]-->[7]--> None
   ^     ^
 previous  previous.next   <- the same shape as every other step

  step 1:  previous.next is 7  ->  previous.next = its next    (do NOT advance)
  [0]-->[7]-->[7]-->[1]-->[7]
  step 2:  previous.next is 7  ->  unlink again
  [0]-->[7]-->[1]-->[7]
  step 3:  previous.next is 7  ->  unlink again
  [0]-->[1]-->[7]
  step 4:  previous.next is 1  ->  KEEP, so advance
  [0]-->[1]-->[7]
              ^ previous
  step 5:  previous.next is 7  ->  unlink
  [0]-->[1]--> None

  return dummy.next  ->  [1]
  return head        ->  [7]-->... the node `head` still refers to. WRONG.
```

What to notice: `previous` never moves during steps 1 to 3. Three deletions in a row happen from the
same standing position, which is exactly what an `if` on the head cannot do and a loop can.

And the builder form, merging `[1, 3]` and `[2, 4]`:

```
  dummy
   |
   v
  [0]                     tail = dummy
   |
   v
  [0]-->[1]               take 1, tail = the 1
   |     ^tail
   v
  [0]-->[1]-->[2]         take 2, tail = the 2
   |           ^tail
   v
  [0]-->[1]-->[2]-->[3]-->[4]
   |
   return dummy.next  ->  [1, 2, 3, 4]

  Not once did the code ask "is this the first node?"
```

---

## 5. The code, built step by step

### Step 1 — the line, and what it means

```python
    dummy = Node(0, head)
    previous = dummy
```

Two lines. `dummy` never moves and is never returned; `previous` is the cursor that walks. Keeping
them as separate names matters — if you walk `dummy` itself forward, you have lost your handle on the
front of the list and cannot return the answer.

### Step 2 — the loop, with the advance rule

```python
    while previous.next is not None:
        if previous.next.value == target:
            previous.next = previous.next.next     # unlink; stay where you are
        else:
            previous = previous.next               # keep; move on
```

The condition looks at `previous.next`, never at `previous`, because `previous` is the joint and
`previous.next` is the wagon. Every delete-by-condition problem in this phase is this loop.

### Step 3 — the return

```python
    return dummy.next
```

Not `head`. If the original head was deleted, `head` still refers to a node that is no longer in the
list.

### Step 4 — the builder form

```python
    dummy = Node(0)
    tail = dummy
    while a is not None and b is not None:
        if a.value <= b.value:
            tail.next, a = a, a.next               # attach a, advance a
        else:
            tail.next, b = b, b.next
        tail = tail.next
```

`tail.next, a = a, a.next` evaluates the right side first, so `a.next` is read before `a` is
reassigned. Written as two statements in the wrong order it loses the rest of `a`. If tuple
assignment makes you nervous under pressure, write it as three explicit lines — clarity beats
cleverness in an interview.

```python
    tail.next = a if a is not None else b          # one list is empty; attach the rest
    return dummy.next
```

The last line is why merging is O(n + m) and not more: whatever remains is already sorted and already
linked, so you attach it whole rather than copying node by node.

### Step 5 — two dummies, for problems that build two lists

Partition List (LeetCode 86) splits a list into "less than x" and "at least x", preserving order.

```python
    less_dummy, more_dummy = Node(0), Node(0)
    less, more = less_dummy, more_dummy
    node = head
    while node is not None:
        target = less if node.value < x else more
        target.next = node
        target = ...                                # see the full version below
```

Two dummies, two cursors, then join. **`more.next = None` at the end is mandatory** — the last node of
the "more" list still points into the original list, and forgetting it builds a cycle.

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


def remove_elements(head: Node | None, target: int) -> Node | None:
    """Remove EVERY node equal to target, including at the head.

    The dummy gives the first real node a predecessor, so the head stops being
    a special case. Two rules:
      - return dummy.next, never head (head may have been deleted)
      - advance `previous` ONLY when you keep a node, or consecutive matches
        leave one behind
    """
    dummy = Node(0, head)
    previous = dummy

    while previous.next is not None:
        if previous.next.value == target:
            previous.next = previous.next.next     # unlink, stay put
        else:
            previous = previous.next               # keep, move on

    return dummy.next


def merge_two_sorted(a: Node | None, b: Node | None) -> Node | None:
    """Merge two sorted lists into one. The BUILDER form of the dummy: `tail`
    needs somewhere to start, so the first node is attached like every other.

    O(n + m) time, O(1) extra space — no nodes are created, only relinked.
    """
    dummy = Node(0)
    tail = dummy

    while a is not None and b is not None:
        if a.value <= b.value:                     # <= keeps the merge STABLE
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next

    tail.next = a if a is not None else b          # attach the rest wholesale
    return dummy.next


def remove_nth_from_end(head: Node | None, n: int) -> Node | None:
    """Remove the nth node from the end in one pass.

    The dummy earns itself twice here: removing the last remaining node is the
    head case, and starting `fast` at the dummy makes the gap arithmetic land
    on the node BEFORE the target rather than on the target.
    """
    dummy = Node(0, head)
    fast = slow = dummy

    for _ in range(n):                             # open a gap of n
        if fast.next is None:
            raise ValueError(f"list has fewer than {n} nodes")
        fast = fast.next

    while fast.next is not None:                   # walk both until fast is last
        fast = fast.next
        slow = slow.next

    slow.next = slow.next.next                     # slow is the predecessor
    return dummy.next


def remove_all_duplicates_sorted(head: Node | None) -> Node | None:
    """From a SORTED list, remove every value that appears more than once.
    [1,2,3,3,4,4,5] -> [1,2,5]. Even the head may be part of a run.
    """
    dummy = Node(0, head)
    previous = dummy
    node = head

    while node is not None:
        if node.next is not None and node.value == node.next.value:
            duplicate = node.value
            while node is not None and node.value == duplicate:
                node = node.next                   # skip the whole run
            previous.next = node                   # unlink all of it at once
        else:
            previous = node
            node = node.next

    return dummy.next


def partition(head: Node | None, x: int) -> Node | None:
    """Reorder so that every node < x comes before every node >= x, keeping the
    relative order within each group. Two dummies, two cursors, then join.
    """
    less_dummy, more_dummy = Node(0), Node(0)
    less, more = less_dummy, more_dummy

    node = head
    while node is not None:
        if node.value < x:
            less.next = node
            less = less.next
        else:
            more.next = node
            more = more.next
        node = node.next

    more.next = None                # MANDATORY: the last "more" node still points
    less.next = more_dummy.next     # into the original list, which would be a cycle
    return less_dummy.next


if __name__ == "__main__":
    print(to_values(remove_elements(from_values([7, 7, 7, 1, 7]), 7)))   # [1]
    print(to_values(remove_elements(from_values([1, 7, 7, 2]), 7)))      # [1, 2]
    print(to_values(remove_elements(from_values([7, 7, 7]), 7)))         # []
    print(to_values(remove_elements(from_values([]), 7)))                # []
    print(to_values(remove_elements(from_values([1, 2, 3]), 7)))         # [1, 2, 3]

    print(to_values(merge_two_sorted(from_values([1, 3, 5]),
                                     from_values([2, 4, 6]))))           # [1,2,3,4,5,6]
    print(to_values(merge_two_sorted(from_values([]), from_values([2])))) # [2]
    print(to_values(merge_two_sorted(None, None)))                        # []

    print(to_values(remove_nth_from_end(from_values([1, 2, 3, 4, 5]), 2)))  # [1,2,3,5]
    print(to_values(remove_nth_from_end(from_values([1, 2, 3, 4, 5]), 5)))  # [2,3,4,5]
    print(to_values(remove_nth_from_end(from_values([9]), 1)))              # []

    print(to_values(remove_all_duplicates_sorted(
        from_values([1, 2, 3, 3, 4, 4, 5]))))                            # [1, 2, 5]
    print(to_values(remove_all_duplicates_sorted(
        from_values([1, 1, 1, 2, 3]))))                                  # [2, 3]

    print(to_values(partition(from_values([1, 4, 3, 2, 5, 2]), 3)))      # [1,2,2,4,3,5]

    # the bug this whole lesson is about
    original = from_values([7, 7, 1])
    result = remove_elements(original, 7)
    print(to_values(result))                  # [1]        <- dummy.next
    print(to_values(original))                # [7, 7, 1]  <- what `return head` gives
```

The last three lines are worth running. `original` still refers to the node it always referred to,
and returning it hands the caller the list with the deleted elements still at the front — no
exception, no warning, just a wrong answer.

---

## 6. What it costs

### Time

```
 remove_elements              O(n)   one pass, one comparison per node
 merge_two_sorted             O(n+m) each node visited once
 remove_nth_from_end          O(n)   one pass, two cursors
 remove_all_duplicates_sorted O(n)   the inner while advances `node`, never restarts
 partition                    O(n)   one pass
```

The inner `while` in `remove_all_duplicates_sorted` deserves a sentence, because it looks quadratic
and is not: it advances the *same* `node` cursor that the outer loop uses, so each node is visited
exactly once across both loops. Same counting argument as the monotonic stack of
[day 071](../day-071-monotonic-stack/README.md).

### Space

```
 the dummy node               1 node, about 48 bytes
 cursors                      2 or 3 references
 -----------------------------------------------------
 extra space                  O(1)
```

**One node, once.** Not one per element, not one per iteration. The most common misunderstanding is
creating a dummy *inside* a loop, which allocates n nodes and does nothing useful.

### What it saves, counted

The version without a dummy, for `remove_elements`:

```
 lines                        11
 loops                         2
 branches for the head         2   (the leading run, and the all-deleted case)
 places the head is referenced 4
```

With a dummy:

```
 lines                         6
 loops                         1
 branches for the head         0
 places the head is referenced 1   (the dummy's constructor)
```

**Two loops become one, and two head branches become none.** That is not a style preference. Each of
those branches is a place where `[7, 7, 7]` or `[]` or `[7]` breaks the function, and the empty and
all-deleted cases are the two an interviewer will try.

### Where the dummy does more than tidy up

In `remove_nth_from_end`, starting `fast` and `slow` at the dummy rather than at the head does two
things at once. It makes "remove the first node" an ordinary case. And it shifts `slow` back by one
so that when `fast` reaches the last node, `slow` is on the **predecessor** of the target rather than
on the target itself — which is exactly where you need to be. Without the dummy you need a gap of
`n + 1` and a separate check for the head, and getting that arithmetic right under pressure is
unpleasant.

---

## 7. The traps

### Trap 1 — `return head` instead of `return dummy.next`

```python
    dummy = Node(0, head)
    ...
    return head                              # WRONG
```

`remove_elements(from_values([7, 7, 1]), 7)` returns `[7, 7, 1]`. The function did all the work
correctly and then handed back a reference to a node that is no longer part of the list. **No error,
wrong answer.** The student teacher counting Sister.

Make it a habit: the moment you write `dummy = Node(0, head)`, write `return dummy.next` as well,
before you write the loop.

### Trap 2 — advancing after a deletion

```python
        if previous.next.value == target:
            previous.next = previous.next.next
        previous = previous.next                 # advances in BOTH cases
```

On `[1, 7, 7, 2]` this returns `[1, 7, 2]`. After unlinking, `previous.next` is a node you have not
inspected, and advancing skips it. **Advance only in the `else`.**

This bug is independent of the dummy and survives every other fix, which is why it deserves its own
sentence in the interview.

### Trap 3 — walking the dummy itself

```python
    dummy = Node(0, head)
    while dummy.next is not None:
        ...
        dummy = dummy.next                       # lost the handle
    return dummy.next                            # returns the tail, or None
```

`dummy` must not move. Use a second name for the cursor. This one usually produces a nearly-empty
result and is obvious the first time you see it — and completely invisible while you are writing it.

### Trap 4 — creating the dummy inside the loop

```python
    while node is not None:
        dummy = Node(0, node)                    # a new one every iteration
```

Allocates `n` nodes, achieves nothing, and often produces correct output, so it survives review. One
dummy, before the loop.

### Trap 5 — forgetting to terminate a built list

```python
    less.next = more_dummy.next
    return less_dummy.next                       # forgot: more.next = None
```

The last node of the "more" chain still points at whatever followed it in the *original* list. Since
that region now precedes it, the result contains a **cycle** and printing it never returns:

```
KeyboardInterrupt
```

after the output list has grown to fill memory. **Any time you build a new list out of existing
nodes, terminate it explicitly.**

### Trap 6 — using a dummy where the list cannot change at the front

Not a bug, just noise. Counting nodes, finding the middle, checking for a cycle — none of these can
change the first node, so a dummy adds a line and buys nothing. **The recognition rule: use a dummy
when the operation can change which node is first, or when you are building a new list.** Otherwise
do not.

### Trap 7 — `dummy = Node(0)` when you meant `Node(0, head)`

```python
    dummy = Node(0)                              # forgot to link the head
    previous = dummy
    while previous.next is not None:             # immediately false
        ...
    return dummy.next                            # None
```

Returns an empty list for every input. Silent, and easy to stare past because the loop looks right.
The guard form is `Node(0, head)`; the builder form is `Node(0)` with nothing attached yet. Know
which one you are writing.

---

## 8. In the interview

### How it gets asked

- The pure case: *"Remove all nodes with a given value."* LeetCode 203. The interviewer will hand you
  `[7, 7, 7, 1, 7]` on purpose.
- The builder case: *"Merge two sorted linked lists."* LeetCode 21, and the follow-up is "now merge
  k lists".
- The one where the dummy does real work: *"Remove the nth node from the end, in one pass."*
  LeetCode 19.
- The hardest: *"Remove all values that appear more than once from a sorted list."* LeetCode 82 —
  even the head can be part of a duplicate run, so an `if` cannot save you.
- The meta version: *"You wrote a dummy node there. Why?"*

### What to say out loud, in the first ninety seconds

1. **Name the problem before the trick.** "The awkward part here is that the node I need to remove
   might be the head, and the head has no predecessor — I cannot unlink a node without holding the one
   before it."
2. **Introduce the dummy as the fix, in one sentence.** "So I put a dummy node in front of the list.
   Now the real head has a predecessor and it is an ordinary node, so one loop handles everything."
3. **Say the return rule immediately.** "And I return `dummy.next`, not `head` — the original head may
   have been deleted, and returning it is a silent wrong answer."
4. **Say the advance rule, as a separate point.** "The other rule in this loop has nothing to do with
   the dummy: after unlinking, I do *not* advance, because `previous.next` is now a node I have not
   looked at. On `[1, 7, 7, 2]`, advancing unconditionally leaves a 7 behind."
5. **State the cost.** "One extra node and O(1) space. It does not change the complexity of anything;
   it removes branches."
6. **Then write it**, which is six lines.

### The follow-ups

**"Why not just handle the head with an `if`?"**
"Because it is not one node — it is a *run*. On `[7, 7, 7, 1]` the first three all have to go, so the
head case is a `while`, not an `if`, and then there is a second special case when everything is
deleted and the head becomes `None`. That is two extra branches and two extra tests. The dummy makes
the count of special cases zero rather than smaller, which is a different kind of win."

**"What is the dummy's value?"**
"It does not matter and it is never read — the loop only ever inspects `previous.next`. I write `0` by
convention. The important part is `dummy.next = head`, and the second important part is that `dummy`
never moves: I walk with a separate cursor, or I lose the handle I need for the return."

**"You used a dummy in merge as well, but nothing is being deleted there."**
"Different job, same idea. When I am *building* a list, the first node is special because there is
nothing to attach it to yet, so the code fills up with 'is this the first?'. A dummy gives the tail
cursor somewhere to start, and then the first node is attached exactly like the fortieth. Delete-form
and build-form are the two uses, and both are 'a node that holds nothing, so that the first one stops
being different'."

**"Show me the input that breaks the naive solution."**
"`[7, 7, 7, 1, 7]` with target 7, for the leading run. `[7, 7, 7]` with target 7, because everything
is deleted and the result must be `None`. `[1, 7, 7, 2]`, which catches the advance-after-delete bug
rather than the head bug. And the empty list. Those four cover it, and I would run them before saying
I was finished."

**"When would you *not* use a dummy?"**
"When the operation cannot change which node is first. Counting the nodes, finding the middle,
detecting a cycle, summing the values — a dummy there is a line that buys nothing and one more thing
for a reader to wonder about. The recognition rule I use is: can the first node change, or am I
building a new list? If neither, no dummy."

**"How does it help in remove-Nth-from-end?"**
"Two ways at once. Removing the last remaining node is the head case, so it is handled for free. And
because both pointers start at the dummy rather than the head, when the fast pointer reaches the last
node the slow pointer is on the *predecessor* of the target instead of on the target — which is
exactly where I need to be to unlink it. Without the dummy I need a gap of n+1 and a separate head
check, and that arithmetic is easy to get wrong under time pressure."

### A model answer

Asked: *remove all nodes with a given value, including at the head.*

> "The awkward part of this problem is not the removal, it is the head. To unlink a node I need the
> node before it, and the head does not have one. And it is worse than a single special case, because
> the head might be part of a *run* — on `[7, 7, 7, 1]` with target seven, the first three all have to
> go, so handling the head with an `if` is not enough; it would have to be a `while`. Then there is a
> second case when every node is deleted and the answer is an empty list.
>
> So instead I put a dummy node in front. One line: `dummy = Node(0, head)`. The value is never read.
> What it buys me is that the real first node now has a predecessor — `dummy` — so it is an ordinary
> node and the single loop that handles the middle handles the front as well. The number of head
> special cases goes from two to zero, which is better than making them shorter.
>
> Two rules come with it and I would state both before writing.
>
> First, I return `dummy.next`, never `head`. The original head may have been deleted, and `head`
> still refers to it, so returning it hands back the list with the removed elements still at the
> front — no exception, just a wrong answer. I write the `return dummy.next` line at the same moment I
> write the dummy, before the loop, so I cannot forget.
>
> Second, and this one is not about the dummy at all: after unlinking a node I must **not** advance the
> cursor. `previous.next` is now a node I have not inspected, so advancing skips it and two
> consecutive matches leave one behind — on `[1, 7, 7, 2]` you get `[1, 7, 2]`. So the advance happens
> only in the branch where I keep a node.
>
> The loop is then four lines: while `previous.next` is not None, if its value matches, unlink and
> stay; otherwise advance.
>
> Complexity is O(n) time — one comparison per node, one pass — and O(1) extra space: exactly one
> dummy node, created once before the loop, not one per iteration.
>
> The inputs I would run before calling it done: `[7, 7, 7, 1, 7]` for the leading run,
> `[7, 7, 7]` where everything goes and the answer is empty, `[1, 7, 7, 2]` for the advance bug,
> `[1, 2, 3]` where nothing matches, and the empty list.
>
> And it is worth saying that the same trick has a second form. When I am *building* a list rather
> than pruning one — merging two sorted lists, say — the first node is special for the mirror reason:
> there is nothing to attach it to. A dummy gives the tail cursor somewhere to start, so the first
> node is attached exactly like every other one, and I return `dummy.next` again. Half the problems in
> this phase are one of those two shapes."

---

## 9. Recall card

- **One line deletes the head special case: `dummy = Node(0, head)`.** The real first node now has a
  predecessor, so it is an ordinary node and **one loop handles everything**. The head case is not
  just an `if` — on `[7, 7, 7, 1]` it is a *run*, plus a second case when everything is deleted. The
  dummy takes the count of special cases to **zero**, not to fewer.
- **`return dummy.next`, never `return head`.** The original head may have been deleted, and returning
  it is a **silent wrong answer** — `remove_elements([7,7,1], 7)` gives back `[7,7,1]`. Write the
  return line at the same moment you write the dummy. And **`dummy` must never move** — walk with a
  separate cursor.
- **The second rule has nothing to do with the dummy: advance ONLY when you keep.** After unlinking,
  `previous.next` is a node you have not inspected, so an unconditional advance leaves consecutive
  matches behind — `[1, 7, 7, 2]` becomes `[1, 7, 2]`.
- **Two forms, one idea — a node that holds nothing so the first one stops being different.** The
  **guard** form is `Node(0, head)`, for pruning. The **builder** form is `Node(0)` plus a moving
  `tail`, for merging, partitioning and copying — and any list you build out of existing nodes must be
  **terminated explicitly** (`more.next = None`) or you construct a cycle and the print never returns.
- **Cost: one node, O(1) space, no complexity change — it removes branches, and branches are where the
  bugs are.** Recognition rule: **use a dummy when the operation can change which node is first, or
  when you are building a new list.** Not for counting, finding the middle, or cycle detection.
  Test inputs that matter: `[7,7,7,1,7]` · `[7,7,7]` · `[1,7,7,2]` · `[]`.
