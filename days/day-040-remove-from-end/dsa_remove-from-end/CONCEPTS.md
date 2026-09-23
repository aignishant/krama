---
day: 40
part: "1.1"
title: "Remove from end"
ids: [DSA-40]
level: working
prerequisites: ["See the linked prerequisite explanation below"]
prev: README.md
next: README.md
failure: true
---

# Remove from end

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Maintain an n-edge gap from a dummy predecessor until the leading pointer reaches the tail; the trailing pointer then precedes the node to remove.

## The story

Deleting the last node is easy until the list has just one node. A dummy predecessor makes removing the head use the same splice as any other removal.

## The idea in plain language

Recall [relative pointer movement](../../day-037-middle-node/dsa_middle-node/CONCEPTS.md)
and [dummy predecessors](../../day-039-merge-linked-lists/dsa_merge-linked-lists/CONCEPTS.md).
This time both pointers move at the same speed after an initial lead. Recognize the pattern
when a position is measured backward from an unknown end and links only move forward.
The contract guarantees a nonempty acyclic chain and 1 <= n <= length.

## Why Krama needs it

This develops DSA-40; the [day hub](../LESSON.md) keeps the tracks independent.
Use the explanation to reason before practice. Reading does not establish study completion.

## The source behind it

[Official LeetCode problem](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) supplies the online contract; [LEETCODE.md](LEETCODE.md) compares its interface with local practice.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The worked examples, proofs, and numeric scenarios below are original teaching material.

## The mechanism

### Worked trace

Let D be a dummy before A -> B -> C -> E, and remove n=2 from the end. Start slow=fast=D,
advance fast exactly two edges to B, then move both while fast.next exists:

| State | slow | fast | Gap |
| --- | --- | --- | --- |
| after lead | D | B | 2 edges |
| first shared step | A | C | 2 edges |
| second shared step | B | E | 2 edges |

Fast is now the tail. Slow is B, the predecessor of C. Set slow.next to slow.next.next,
bypassing C, then return dummy.next. The gap remains n because both move one edge per round.
Number real nodes 1..L and dummy 0: final fast position L implies slow position L-n.
Its successor L-n+1 is exactly the nth node from the end.

For n=L, fast reaches the tail during its initial lead, so slow stays dummy and the head
is removed. For n=1, slow finishes just before the tail. With a singleton and n=1, the
returned head becomes None. Use L for list length to avoid confusing it with the input rank n.

A two-pass baseline counts L then finds predecessor L-n; it also takes O(L) time and O(1)
traversal state. The fixed gap needs no preliminary counting pass. Building local nodes and
serializing still require O(L) memory/output storage. Online returns the new head; local
practice returns a list of remaining values. Both require valid n. Empty input or invalid n
needs a separately specified policy before it can be treated as a required test.

An alternative initializes fast n+1 edges ahead and stops at None. That is valid with its
own invariant, but mixing its stopping rule with this n-edge initialization removes the wrong
node. Count edges and state what slow denotes before coding.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
class Node:
    def __init__(self, value, next=None):
        self.value, self.next = value, next

head = Node('A', Node('B', Node('C')))
dummy = Node(None, head)
slow = fast = dummy
fast = fast.next  # n=1: a one-edge gap
while fast.next is not None:
    slow, fast = slow.next, fast.next
print('predecessor, target:', slow.value, slow.next.value)
assert slow.value == 'B' and slow.next.value == 'C'
slow.next = slow.next.next
assert head.next.next is None
single = Node('only')
dummy = Node(None, single)
dummy.next = dummy.next.next
print('old head still exists:', single.value)
print('returned head:', dummy.next)
assert dummy.next is None
```

**Line by line:** The first chain checks the gap and predecessor before unlinking its last node. The singleton then exposes a common return bug: the old head object still exists through an alias, but the correct returned head is dummy.next, now None.

Observed author output on Python 3.12.10, 2026-09-23:

```text
predecessor, target: B C
old head still exists: only
returned head: None
```

These are author teaching observations. The deterministic models do not measure production
performance or prove the behavior of a deployed cache or concurrent service.

## In production

Unlinking changes reachability from the returned head; it does not erase an object held by
another reference. Define ownership if external callers keep node handles. Optional validation
of n changes the API contract and may require detecting an exhausted lead safely; the exercise
itself guarantees a valid rank.

## Check yourself

### Readiness before practice

1. With length five and n=5, where do both pointers stop?
2. Why does returning the original head fail for a singleton?
3. What changes if fast stops at None instead of the tail?

Return to [README.md](README.md) for the assignment, verification, and evidence route.
Keep the independent 60/30/15-minute budgets; extra depth can wait for another sitting.
