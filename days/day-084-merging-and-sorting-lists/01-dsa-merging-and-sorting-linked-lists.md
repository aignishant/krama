---
day: 84
track: dsa
title: "Merging and sorting linked lists"
phase: "Linked lists"
status: written
---

# Day 084 · DSA — Merging and sorting linked lists

**After today you can:** You can merge two sorted lists and sort a list in O(n log n) without extra arrays.

**The interviewer asks it as:** *Merge two sorted linked lists. Now sort an unsorted one.*

---

## 1. What this is, and why they ask it

Merging two sorted linked lists is the easiest hard-sounding problem there is: walk both, always take
the smaller front node, and when one runs out attach the rest of the other in one assignment. No nodes
are created and nothing is copied — you relink what already exists.

Then the follow-up turns it into the real question: **sort an unsorted linked list.** Split it in
half, sort each half, merge. That is **merge sort**, and on a linked list it is not merely one option
among several — it is the *right* one, for a reason worth being able to state: quicksort needs random
access to partition efficiently, and a linked list has none, while merge sort needs only sequential
access and, unlike on an array, needs no scratch space to merge into.

They ask it because it composes three days in a row. The dummy-head builder from
[day 080](../day-080-dummy-head/README.md) does the merge, the runner from
[day 082](../day-082-runner-technique/README.md) does the split, and the whole thing is
[day 053](../day-053-merge-sort/README.md)'s merge sort with pointers instead of slices. It is
LeetCode 21, 148 and 23, and "merge k sorted lists" is one of the most-asked hard questions at Amazon
and Google.

---

## 2. The story

The tomato section of the mandi opens at four in the morning and Basavaraj has graded there for
twenty-two years.

The buyers want them in a line on the tray, smallest at one end and largest at the other, because a
hotel man walking past can then take his eighty from the middle without picking through anything.

Two farmers bring tomatoes on a Tuesday. Both of them have already graded their own — each basket is
in order, small to large, because they do it at home while the lorry is loading. What Basavaraj has to
do is make one line out of two.

He does not tip both baskets out and start again. He has watched people do that and it takes forty
minutes.

He puts a hand over each basket, takes whichever of the two front tomatoes is smaller, and lays it
down. Then again. And again. He is not comparing anything except two tomatoes at a time, and he never
looks back at what he has already laid down, because whatever he laid down last was the smallest of
everything remaining and nothing smaller can turn up now.

When one basket runs out, he stops comparing entirely. He tips the rest of the other basket straight
onto the end of the line, in the order it is already in, because it is already in order and there is
nothing left to compare it against. That part takes four seconds and it is most of the second basket.

His nephew asked him once how the farmers get their baskets sorted at home in the first place, since
they are dealing with three hundred tomatoes and no line.

Basavaraj said nobody sorts three hundred tomatoes. What his brother-in-law does is put them in pairs
— just two, decide which is smaller, that is a sorted pair. Then he pushes two pairs together the same
way Basavaraj pushes two baskets together, and gets a sorted four. Then two fours into an eight. He
keeps doubling. By the time he has been at it half an hour there are two big graded rows and one last
push, and the basket is done.

The only skill in the whole thing, Basavaraj says, is the two hands over the two baskets. Everything
else is doing that again with bigger baskets.

---

## 3. The idea in plain English

Basavaraj's two hands are the merge. His brother-in-law doubling from pairs is the sort. That is the
entire lesson, and the second is built from the first.

### Merging two sorted lists

Walk both, always take the smaller head:

```python
    dummy = Node(0)
    tail = dummy
    while a is not None and b is not None:
        if a.value <= b.value:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a is not None else b       # the rest, in one assignment
    return dummy.next
```

Three things are worth saying about those nine lines.

**The dummy is the builder form** from [day 080](../day-080-dummy-head/README.md): `tail` needs
somewhere to start, so the first node is attached exactly like the fortieth and there is no "is this
the first one?" branch.

**The last line is Basavaraj tipping the basket in.** Whatever remains is already sorted and already
linked, so you attach the whole chain with one assignment. Looping to move it node by node is correct
and pointless, and noticing that is the difference between having understood the merge and having
copied it.

**`<=` not `<` keeps the merge stable.** When two values are equal, taking from `a` first preserves
the original relative order. Stability is invisible on integers and matters the moment the nodes carry
anything else, and it is what makes merge sort stable. Say it.

**Nothing is allocated.** No new nodes, no arrays, no copies of values — only `next` pointers are
rewritten. That is the property that makes this O(1) extra space, and it is exactly what an array
merge cannot do.

### Sorting: split, sort, merge

```python
def sort(head):
    if head is None or head.next is None:
        return head                     # 0 or 1 nodes is already sorted
    left, right = split_in_half(head)
    return merge(sort(left), sort(right))
```

Five lines, and every one of them is a day you have already done. The split uses the runner technique
from [day 082](../day-082-runner-technique/README.md), and it must find the **first** middle:

```python
    slow = fast = head
    while fast.next is not None and fast.next.next is not None:
        slow, fast = slow.next, fast.next.next
    second = slow.next
    slow.next = None                    # THE CUT — mandatory
    return head, second
```

Two details, both fatal if missed.

**The first middle, not the second.** With the second middle, a two-node list splits into itself and
an empty list, the recursion never shrinks, and you get `RecursionError`.

**The cut.** Without `slow.next = None`, the two "halves" share every node from the middle onwards, so
both halves are really the whole list and the recursion again never terminates.

### Why merge sort and not quicksort

This is the question the interviewer is heading for, and the answer is about **access**, not about
worst cases.

**Quicksort on an array** partitions in place by swapping elements at two indices moving toward each
other. That needs random access — `arr[i]` and `arr[j]` in constant time — and a linked list has
none. You *can* write a linked-list quicksort by building three lists (less, equal, greater) in one
pass and concatenating, and it works, but it is O(n²) in the worst case and its pivot choice is worse
because you cannot cheaply sample the middle element.

**Merge sort on a linked list** needs only sequential access, which is all a list offers. And here is
the part that is *better* on a list than on an array: merging two arrays needs a third array to merge
into, so array merge sort is O(n) extra space. Merging two linked lists needs **no space at all** —
you relink existing nodes.

```
                       array           linked list
 quicksort             O(n log n) avg  awkward: no random access, O(n²) worst
 merge sort            O(n log n)      O(n log n)
 merge sort extra      O(n) scratch    O(1) — pointers only
```

**Merge sort is the linked list's best case and the array's worst case for space.** That inversion is
the answer, and it is why `sort()` on a linked list is a merge sort in every standard library that
has one.

### The recursion's space, and how to remove it

The recursive version uses `O(log n)` stack frames — depth `log₂ n`, so about 20 at a million nodes.
That is small, and it is not O(1), and an interviewer asking for strictly constant space wants the
**bottom-up** version:

```
 pass 1:  merge sublists of size 1  ->  sorted runs of 2
 pass 2:  merge sublists of size 2  ->  sorted runs of 4
 pass 3:  merge sublists of size 4  ->  sorted runs of 8
 ...      log n passes
```

Basavaraj's brother-in-law making pairs, then fours, then eights. No recursion, no stack, `O(1)` extra
space — at the cost of considerably fiddlier code, because each pass has to cut out two runs of the
right size, merge them, and stitch the result back into a growing output.

Write the recursive one first. Mention the bottom-up one and its trade honestly: *log n stack frames
against about twenty lines of extra bookkeeping.*

### Merging k sorted lists

The escalation, and it has three answers of increasing quality.

**One at a time.** Merge list 1 with list 2, then that with list 3, and so on. Each merge walks
everything merged so far, so the total is `n + 2n + 3n + … = O(k²n/k)` — for `k` lists of `n/k` nodes
each, that is **O(nk)**. On 10,000 lists this is hopeless.

**A min-heap of the k current heads.** Pop the smallest, attach it, push its successor. Each of the `n`
nodes goes through a heap of size `k`, so **O(n log k)**. This is the standard answer.

**Divide and conquer.** Merge lists in pairs, then merge the results in pairs, and so on —
`log k` rounds, each touching all `n` nodes, so also **O(n log k)**, with no heap and no extra data
structure at all. Slightly faster in practice and much easier to get right.

Give the heap answer and then say you would probably write the pairwise one, because it reuses the
two-list merge you have already written and has nothing to go wrong.

---

## 4. The picture

Merging `[1, 3, 5]` and `[2, 4]`.

```
  a: [1] -> [3] -> [5] -> None
  b: [2] -> [4] -> None

  dummy -> ?                          tail = dummy

  1 <= 2   take a       dummy -> [1]                    a = [3], tail = [1]
  3 >  2   take b       dummy -> [1] -> [2]             b = [4], tail = [2]
  3 <= 4   take a       dummy -> [1] -> [2] -> [3]      a = [5], tail = [3]
  5 >  4   take b       ... -> [4]                      b = None, tail = [4]

  b is exhausted -> tail.next = a       ONE assignment attaches [5]

  result: [1] -> [2] -> [3] -> [4] -> [5]

  nodes created: 0.  values copied: 0.  only `next` pointers were rewritten.
```

What to notice: the final step attached the whole of what was left of `a` with one assignment.
Basavaraj tipping the basket in. On a merge where one list is much longer than the other, that single
line does most of the work.

The sort, drawn as the recursion tree on `[4, 2, 1, 3]`:

```
 split                    [4, 2, 1, 3]
                         /             \
                    [4, 2]             [1, 3]
                    /    \             /    \
                  [4]    [2]         [1]    [3]

 merge             \      /           \      /
                    [2, 4]             [1, 3]
                         \             /
                          [1, 2, 3, 4]

 depth = log2(4) = 2 levels of splitting
 each level does O(n) work merging
 -> O(n log n)
```

What to notice: **every level does exactly `n` units of work**, because every node is looked at once
per level, and there are `log₂ n` levels. That is the whole complexity argument, in a picture.

And the split, where both mistakes live:

```
 [1] -> [2] -> [3] -> [4]

 FIRST middle  (while fast.next and fast.next.next)   slow ends on [2]
   second = [3];  slow.next = None
   -> [1, 2]  and  [3, 4]              both halves shrink.  Correct.

 SECOND middle (while fast and fast.next)             slow ends on [3]
   -> [1, 2, 3]  and  [4]              still shrinks here, BUT on [1, 2]:
                                        slow ends on [2], second = None
                                        -> [1, 2] and []  — no shrink, infinite recursion

 NO CUT (forgetting slow.next = None)
   -> "[1, 2]" is really [1, 2, 3, 4] because it still points onward
      both halves are the whole list.  Infinite recursion.
```

---

## 5. The code, built step by step

### Step 1 — the merge, and the line that does the most work

```python
    tail.next = a if a is not None else b
```

Written before the loop in your head, not after. It is the reason the merge is O(n + m) rather than
something worse, and it is the line that shows you understood that the remainder is already sorted.

### Step 2 — the split, with the cut written immediately

```python
    second = slow.next
    slow.next = None
```

Two lines, always together. Write the cut in the same keystroke as the split or you will forget it,
and forgetting it does not raise — it hangs.

### Step 3 — the recursion, and its base case

```python
    if head is None or head.next is None:
        return head
```

**Both conditions.** `head is None` for an empty list; `head.next is None` for a single node. Without
the second, `split_in_half` on one node returns the node and `None`, and `sort(None)` returns `None`,
and the merge is fine — but the recursion has not shrunk on the way in, and some formulations spin.
Write both.

### Step 4 — merging k lists, pairwise

```python
    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            first = lists[i]
            second = lists[i + 1] if i + 1 < len(lists) else None
            merged.append(merge_two(first, second))
        lists = merged
    return lists[0] if lists else None
```

Six lines, no heap, and it reuses `merge_two` unchanged. The `if i + 1 < len(lists)` handles an odd
count by merging the last list with `None`, which `merge_two` already handles correctly — so there is
no special case.

### Step 5 — bottom-up, for strict O(1) space

```python
    size = 1
    while size < length:
        dummy = Node(0)
        tail, current = dummy, head
        while current is not None:
            left = current
            right = _split_off(left, size)          # cut `size` nodes, return the rest
            current = _split_off(right, size)
            tail = _append_merged(tail, merge_two(left, right))
        head = dummy.next
        size *= 2
    return head
```

Two nested loops: the outer doubles the run length, the inner walks the list cutting out pairs of runs.
Every cut is a `next = None`, and every stitch is one assignment. It is genuinely fiddlier, and it is
the honest answer to "can you do it in O(1) space".

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


def merge_two(a: Node | None, b: Node | None) -> Node | None:
    """Merge two sorted lists into one sorted list.

    Nothing is created and nothing is copied — only `next` pointers move, so
    this is O(1) extra space, which an array merge cannot manage.

    `<=` rather than `<` keeps the merge STABLE: equal values keep their
    original relative order, which is what makes merge sort stable.
    """
    dummy = Node(0)
    tail = dummy

    while a is not None and b is not None:
        if a.value <= b.value:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next

    tail.next = a if a is not None else b    # the rest is already sorted: one assignment
    return dummy.next


def split_in_half(head: Node) -> tuple[Node, Node | None]:
    """Cut at the FIRST middle, so both halves are strictly smaller.

    The second middle would leave [1,2] as [1,2] and [], and the recursion
    would never terminate. The cut is mandatory for the same reason.
    """
    slow = fast = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next
    second = slow.next
    slow.next = None                          # THE CUT
    return head, second


def sort(head: Node | None) -> Node | None:
    """Merge sort. O(n log n) time, O(log n) stack space.

    Merge sort rather than quicksort because a linked list has no random
    access — and because merging lists needs no scratch space at all, where
    merging arrays needs a second array.
    """
    if head is None or head.next is None:     # both conditions
        return head
    left, right = split_in_half(head)
    return merge_two(sort(left), sort(right))


def merge_k_pairwise(lists: list[Node | None]) -> Node | None:
    """Merge k sorted lists. O(n log k) time, and it reuses merge_two unchanged.

    Merging them one at a time would be O(nk): each merge re-walks everything
    merged so far. Pairwise rounds halve the number of lists each time, so
    every node is touched log k times.
    """
    lists = [item for item in lists if item is not None]
    if not lists:
        return None

    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            second = lists[i + 1] if i + 1 < len(lists) else None
            merged.append(merge_two(lists[i], second))   # merge_two handles None
        lists = merged
    return lists[0]


def merge_k_heap(lists: list[Node | None]) -> Node | None:
    """The same thing with a min-heap of the current heads. Also O(n log k).

    The `index` in the tuple is a tie-breaker: without it, Python compares the
    Node objects when two values are equal and raises TypeError.
    """
    import heapq

    heap: list[tuple[int, int, Node]] = []
    for index, node in enumerate(lists):
        if node is not None:
            heapq.heappush(heap, (node.value, index, node))

    dummy = Node(0)
    tail = dummy
    while heap:
        _, index, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next is not None:
            heapq.heappush(heap, (node.next.value, index, node.next))
    tail.next = None                          # the last node still points into its old list
    return dummy.next


def sort_bottom_up(head: Node | None) -> Node | None:
    """Merge sort with no recursion: O(n log n) time, O(1) space.

    Pass 1 merges runs of 1 into runs of 2, pass 2 merges 2s into 4s, and so
    on for log n passes. Fiddlier, and it is the honest answer to "strictly
    constant space".
    """
    if head is None or head.next is None:
        return head

    length = 0
    node = head
    while node is not None:
        length += 1
        node = node.next

    dummy = Node(0, head)
    size = 1
    while size < length:
        previous, current = dummy, dummy.next
        while current is not None:
            left = current
            right = _cut(left, size)          # left keeps `size` nodes; right is the rest
            current = _cut(right, size)       # right keeps `size` nodes; current is the rest
            previous.next = merge_two(left, right)
            while previous.next is not None:
                previous = previous.next      # walk to the end of what we just merged
        size *= 2
    return dummy.next


def _cut(head: Node | None, size: int) -> Node | None:
    """Keep `size` nodes on `head`, cut them off, and return the remainder."""
    node = head
    while size > 1 and node is not None:
        node = node.next
        size -= 1
    if node is None:
        return None
    rest = node.next
    node.next = None
    return rest


if __name__ == "__main__":
    print(to_values(merge_two(from_values([1, 3, 5]), from_values([2, 4]))))  # [1,2,3,4,5]
    print(to_values(merge_two(from_values([]), from_values([2]))))            # [2]
    print(to_values(merge_two(None, None)))                                   # []
    print(to_values(merge_two(from_values([1, 1]), from_values([1]))))        # [1, 1, 1]

    left, right = split_in_half(from_values([1, 2, 3, 4]))
    print(to_values(left), to_values(right))                                  # [1, 2] [3, 4]
    left, right = split_in_half(from_values([1, 2, 3]))
    print(to_values(left), to_values(right))                                  # [1, 2] [3]
    left, right = split_in_half(from_values([1, 2]))
    print(to_values(left), to_values(right))                                  # [1] [2]

    print(to_values(sort(from_values([4, 2, 1, 3]))))            # [1, 2, 3, 4]
    print(to_values(sort(from_values([-1, 5, 3, 4, 0]))))        # [-1, 0, 3, 4, 5]
    print(to_values(sort(from_values([2, 2, 1, 1]))))            # [1, 1, 2, 2]
    print(to_values(sort(from_values([1]))))                     # [1]
    print(to_values(sort(None)))                                 # []

    print(to_values(sort_bottom_up(from_values([4, 2, 1, 3, 9, 7]))))   # [1,2,3,4,7,9]

    ks = [from_values([1, 4, 5]), from_values([1, 3, 4]), from_values([2, 6])]
    print(to_values(merge_k_pairwise(ks)))                       # [1,1,2,3,4,4,5,6]
    ks = [from_values([1, 4, 5]), from_values([1, 3, 4]), from_values([2, 6])]
    print(to_values(merge_k_heap(ks)))                           # [1,1,2,3,4,4,5,6]
    print(to_values(merge_k_pairwise([])), to_values(merge_k_pairwise([None])))   # [] []

    import random
    for _ in range(2000):
        sample = [random.randint(-20, 20) for _ in range(random.randint(0, 15))]
        assert to_values(sort(from_values(sample))) == sorted(sample), sample
        assert to_values(sort_bottom_up(from_values(sample))) == sorted(sample), sample
    print("both sorts agreed with sorted() on 2000 random inputs")
```

---

## 6. What it costs

### Merging two lists

```
 time:   every node from each list is attached exactly once  ->  O(n + m)
 space:  one dummy node and one tail reference               ->  O(1)
```

Compare with merging two **arrays**, which is also O(n + m) time but needs an O(n + m) output array,
because you cannot write into either input without destroying what you have not read yet. **The linked
list version needs no scratch space**, and that single difference is why merge sort behaves better on
lists than on arrays.

### Sorting

```
 splitting:  O(n) per level, walking to find the middle
 merging:    O(n) per level, every node attached once
 levels:     log2(n)
 ---------------------------------------------------
 time:       O(n log n)
 space:      O(log n) recursion stack   (O(1) bottom-up)
```

Count it out: at n = 1,000,000, `log₂ n` is about 20, so twenty levels of `n` work each — about
2 × 10⁷ node visits, and twenty stack frames.

Against the alternatives:

```
 copy values to a list, sort, write back:  O(n log n) time, O(n) SPACE, n writes
 merge sort in place:                      O(n log n) time, O(log n) space, 0 allocations
 bubble/insertion sort on the list:        O(n²) — 10^12 at n = 10^6
```

The first is a legitimate answer if you say what you traded. It is also usually what the interviewer is
testing you *not* to reach for.

### Merging k lists

```
 one at a time:  merge 1+2, then that + 3, ...
                 total node visits = n/k * (1 + 2 + ... + k) ≈ n·k/2   ->  O(nk)
 heap of heads:  each of n nodes pushed and popped once, heap size k   ->  O(n log k)
 pairwise:       log2(k) rounds, each touching all n nodes             ->  O(n log k)
```

```
 k = 10,000 lists, n = 1,000,000 nodes:
   one at a time:  ~5 × 10^9 operations
   O(n log k):     10^6 × 13  ≈  1.3 × 10^7
   ratio:          about 380x
```

And between the two good answers: the heap does `n` pushes and `n` pops with a comparison-heavy
constant, while pairwise does plain merges. **Pairwise is usually faster in practice and has nothing
to go wrong**, which is why it is worth naming even though the heap is the "expected" answer.

### Stability

Merge sort is stable when the merge uses `<=`, and that is free — one character. Quicksort is not
stable without extra work. On a list of records sorted by one key and then another, stability is the
difference between a correct result and a subtly wrong one, and it is worth one sentence.

---

## 7. The traps

### Trap 1 — splitting at the second middle

```python
    while fast is not None and fast.next is not None:      # the SECOND middle
```

On `[1, 2]`, `slow` ends on node 2, so `second` is `None` and the "halves" are `[1, 2]` and `[]`. The
recursion does not shrink:

```
RecursionError: maximum recursion depth exceeded
```

**For splitting, always the first middle.** This is the same distinction as
[day 082](../day-082-runner-technique/README.md), and this is the problem where getting it wrong is
fatal rather than merely different.

### Trap 2 — forgetting the cut

```python
    second = slow.next
    return head, second                     # forgot: slow.next = None
```

Both halves are the whole list, because the first still points onward into the second. Same
`RecursionError`, different cause, and it is harder to see because the split *looks* right.

### Trap 3 — looping to attach the remainder

```python
    while a is not None:                    # instead of tail.next = a
        tail.next = a
        a = a.next
        tail = tail.next
```

Correct, and it does node-by-node work for something one assignment achieves. Worse, it signals that
you have not noticed the remainder is already sorted and already linked — which is the one insight the
merge is testing.

### Trap 4 — `<` instead of `<=`

Both produce a correctly sorted list of integers. `<` takes from `b` when values are equal, which
reverses the relative order of equal elements and makes the sort **unstable**. Invisible on numbers,
wrong on records. One character, and worth saying out loud.

### Trap 5 — the heap comparing Node objects

```python
    heapq.heappush(heap, (node.value, node))       # no tie-breaker
```

```
TypeError: '<' not supported between instances of 'Node' and 'Node'
```

Fires the moment two nodes have equal values, because Python falls through to comparing the second
element of the tuple. Add an index or a counter as a tie-breaker. This is the single most common bug in
"merge k sorted lists".

### Trap 6 — the heap version not terminating the output

```python
    while heap:
        ...
        tail = node
    return dummy.next                        # forgot: tail.next = None
```

The final node still points into whatever followed it in its original list, so the result silently
includes nodes that were already merged — or loops. Any list you build out of existing nodes must be
terminated explicitly, exactly as in [day 080](../day-080-dummy-head/README.md)'s partition.

### Trap 7 — the base case with only one condition

```python
    if head is None:
        return head                          # missing: or head.next is None
```

A single-node list is split into itself and `None`, and `sort` is called on the same single node again.
Depending on how the split is written this either recurses for ever or does redundant work. Both
conditions, always.

### Trap 8 — copying values into a Python list "just to sort it"

```python
    values = sorted(to_values(head))
    return from_values(values)
```

O(n) extra space and `n` new nodes. It is a legitimate answer if you say what you traded — and it is
almost always the thing the question exists to test you *not* to do. If you write it, write it as the
baseline and then improve it.

### Trap 9 — reaching for quicksort

Partitioning a linked list by swapping at two moving indices is not possible without random access.
The three-list version (less, equal, greater) does work, but it is O(n²) in the worst case and its
pivot selection is worse because sampling the middle costs O(n). **Merge sort is the correct choice
here and you should be able to say why in one sentence**, rather than because you happened to remember
it.

---

## 8. In the interview

### How it gets asked

- The warm-up: *"Merge two sorted linked lists."* LeetCode 21, five minutes.
- The main question: *"Sort a linked list in O(n log n) time."* LeetCode 148, and then *"…and O(1)
  space"*, which is asking for bottom-up.
- The hard one: *"Merge k sorted linked lists."* LeetCode 23.
- The reasoning probe, which is the real test: *"Why merge sort rather than quicksort?"*
- The stability probe: *"Is your sort stable? Does it matter?"*

### What to say out loud, in the first ninety seconds

1. **For the merge, name what you are not doing.** "I am not creating any nodes or copying any values —
   I am relinking the existing ones, so this is O(1) extra space."
2. **Say the dummy's job.** "A dummy head so the first node is attached like every other one, and I
   return `dummy.next`."
3. **Say the remainder line before you write it.** "When one list runs out, the other is already sorted
   and already linked, so I attach the whole thing with one assignment rather than looping."
4. **For the sort, name the three pieces.** "Split with the fast and slow pointers, sort each half
   recursively, merge. That is merge sort, and it is five lines because I already have the merge."
5. **Pre-empt the quicksort question.** "Merge sort rather than quicksort, because quicksort's
   partition wants random access and a list has none — and because merging lists needs no scratch
   space, whereas merging arrays needs a second array. Merge sort is the list's best case."
6. **Flag the two fatal split details.** "Two things I have to get right: the *first* middle, so both
   halves shrink, and the cut, so they are actually separate lists."

### The follow-ups

**"Why merge sort and not quicksort?"**
"Two reasons, and the second is the interesting one. First, quicksort partitions by moving two indices
toward each other and swapping, which needs random access — a linked list has none, and walking to an
index is O(n). You can write a list quicksort by building three sublists, but it is O(n²) in the worst
case and you cannot cheaply sample a good pivot. Second, and this is what makes merge sort actively
*good* here rather than merely possible: merging two arrays needs a third array to write into, so array
merge sort costs O(n) scratch space. Merging two linked lists costs nothing, because you relink
existing nodes. Merge sort is the array's worst case for space and the list's best."

**"Can you do it in O(1) space?"**
"The recursive version is O(log n) stack — about twenty frames at a million nodes — so strictly it is
not constant. For genuinely O(1) I would go bottom-up: pass one merges runs of size 1 into runs of 2,
pass two merges 2s into 4s, and so on for log n passes, with no recursion. Same O(n log n) time, no
stack, and about twenty lines more code because each pass has to cut out two runs of the right size and
stitch the result back in. I would write the recursive one first and offer this if constant space is a
hard requirement."

**"Is your sort stable?"**
"Yes, because the merge takes from the first list when values are equal — `<=` rather than `<`. That
is one character and it is free. It is invisible when the nodes hold integers, and it is the difference
between right and wrong when they hold records that were already ordered by another key. Quicksort is
not stable without extra work, which is another reason not to reach for it here."

**"Now merge k sorted lists."**
"Three answers. Merging one at a time is O(nk), because each merge re-walks everything merged so far —
at ten thousand lists and a million nodes that is about five billion operations. A min-heap of the
current heads is O(n log k): each node is pushed and popped once from a heap of size k. Or divide and
conquer — merge them in pairs, then merge the results in pairs, for log k rounds, which is also
O(n log k). I would write the pairwise one, because it reuses the two-list merge unchanged and has
nothing to go wrong. The heap version has a trap: you must include a tie-breaker in the tuple, or
Python compares two Node objects when values are equal and raises TypeError."

**"What is the complexity, and where does the `log n` come from?"**
"Each level of the recursion does O(n) work — every node is walked once during splitting and attached
once during merging — and the depth is log₂ n, because the list halves each time. So O(n log n). At a
million nodes that is twenty levels of a million, about two times ten to the seven node visits. Space
is O(log n) for the stack, not O(n), because nothing is allocated per level."

**"Why not just copy the values into an array and sort that?"**
"You can, and it is O(n log n) too. What it costs is O(n) extra space plus rebuilding the list, and it
throws away node identity — anything holding a reference to a specific node now points into the old
structure. I would say it as the baseline and then give the in-place version, because the in-place one
is what the question is asking for."

### A model answer

Asked: *merge two sorted linked lists, then sort an unsorted one.*

> "The merge first. I walk both lists and always take whichever front node is smaller, attaching it to
> the end of the result. The important thing to say is what I am *not* doing: I am not creating any
> nodes and not copying any values. Only `next` pointers move, so this is O(1) extra space — which an
> array merge cannot manage, and that turns out to matter for the second half of the question.
>
> Two details in the loop. I use a dummy head so the tail cursor has somewhere to start and the first
> node is attached exactly like every other, and I return `dummy.next`. And when one list runs out, I
> attach *the whole remainder* with a single assignment rather than looping — whatever is left is
> already sorted and already linked, so there is nothing to do to it.
>
> One more: I compare with `<=`, not `<`, so that when values are equal I take from the first list.
> That keeps the merge stable, which is invisible on integers and matters as soon as the nodes carry
> records.
>
> Now sorting. Split the list in half, sort each half, merge the two results. That is merge sort, and
> it is five lines because the merge already exists.
>
> Two things in the split are fatal if I get them wrong. I must take the *first* middle, not the
> second — with the second, a two-node list splits into itself and an empty list, the recursion never
> shrinks, and it blows the stack. And I must cut: set the first half's last node's `next` to `None`,
> or the two halves are really the same list and it never terminates either. I write the cut in the
> same breath as the split for that reason.
>
> Why merge sort and not quicksort — I think that is the actual question. Quicksort partitions by
> moving two indices toward each other and swapping, which needs random access, and a linked list has
> none. You can write a list quicksort with three sublists, and it is O(n²) in the worst case with a
> pivot you cannot choose well. But the better reason is the other way round: merging two arrays needs
> a third array to write into, so array merge sort costs O(n) scratch space. Merging two lists costs
> nothing. Merge sort is the array's worst case for space and the linked list's best.
>
> Complexity: every level does O(n) work and there are log₂ n levels, so O(n log n). Space is O(log n)
> for the recursion — about twenty frames at a million nodes. If you want strictly O(1), the bottom-up
> version merges runs of one into runs of two, then twos into fours, with no recursion; same time, no
> stack, and about twenty more lines of bookkeeping.
>
> Before I called it done I would run: an empty list, a single node, two nodes, all-equal values, and
> already-sorted input — and I would cross-check against Python's `sorted` on a few thousand random
> inputs, because the split is exactly the kind of code that is right on the cases you think of and
> wrong on the ones you do not."

---

## 9. Recall card

- **The merge creates nothing and copies nothing — only `next` pointers move, so it is O(1) extra
  space.** Use a **dummy builder** so the first node attaches like every other, `<=` **not** `<` so the
  merge is **stable**, and attach the remainder **in one assignment** (`tail.next = a if a else b`),
  because whatever is left is already sorted and already linked.
- **Sort = split, sort each half, merge — five lines, all of them days you have already done.** Two
  fatal details in the split: the **FIRST middle** (`while fast.next and fast.next.next`), or `[1,2]`
  splits into itself and nothing and you get `RecursionError`; and **the cut** (`slow.next = None`), or
  both halves are the whole list. Base case needs **both** `head is None` **and** `head.next is None`.
- **Why merge sort, in one sentence each.** Quicksort's partition needs **random access**, which a list
  does not have. And merging **arrays** needs a scratch array while merging **lists** needs nothing —
  so **merge sort is the array's worst case for space and the list's best.**
- **O(n log n) time — every level does `n` work, and there are `log₂ n` levels (≈20 at a million
  nodes).** Space is **O(log n)** stack, not O(1); the **bottom-up** version (merge runs of 1 → 2 → 4 …)
  is genuinely O(1) at the cost of ~20 fiddlier lines. Copying values into a Python list is O(n) space
  and throws away node identity.
- **Merge k lists: one at a time is O(nk) (~5 × 10⁹ at k = 10⁴, n = 10⁶); a heap of the k heads is
  O(n log k); pairwise rounds are also O(n log k) and reuse `merge_two` unchanged** — prefer pairwise.
  The heap's trap: **include a tie-breaker in the tuple** or `TypeError: '<' not supported between
  instances of 'Node'`, and **terminate the output** with `tail.next = None`.
