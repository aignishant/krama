---
day: 39
part: "1.1"
title: "Merge linked lists"
ids: [DSA-39]
level: working
prerequisites: ["See the linked prerequisite explanation below"]
prev: README.md
next: README.md
failure: true
---

# Merge linked lists

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Keep the last committed output node and splice the smaller remaining head after it, then attach the unconsumed suffix.

## The story

A merge prints the right values but quietly allocates replacement nodes. The caller holding an original node discovers that its identity was discarded.

## The idea in plain language

Recall [saving references before rewiring](../../day-036-reverse-a-linked-list/dsa_reverse-a-linked-list/CONCEPTS.md).
Two sorted chains expose their smallest remaining values at their heads. A tail reference
marks the end of the committed output prefix; a dummy node supplies an initial predecessor.
The dummy is temporary bookkeeping, never part of the returned values. This fits sorted,
acyclic, disjoint inputs when mutation is allowed.

## Why Krama needs it

This develops DSA-39; the [day hub](../LESSON.md) keeps the tracks independent.
Use the explanation to reason before practice. Reading does not establish study completion.

## The source behind it

[Official LeetCode problem](https://leetcode.com/problems/merge-two-sorted-lists/) supplies the online contract; [LEETCODE.md](LEETCODE.md) compares its interface with local practice.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The worked examples, proofs, and numeric scenarios below are original teaching material.

## The mechanism

### Worked trace

Use A1(2) -> A2(6) and B1(2) -> B2(5). Choose A on equality for a deterministic tie rule.

| Step | Selected node | Committed prefix | Remaining heads |
| --- | --- | --- | --- |
| 1 | A1 | A1 | A2, B1 |
| 2 | B1 | A1 -> B1 | A2, B2 |
| 3 | B2 | A1 -> B1 -> B2 | A2, None |
| Finish | attach A2 | A1 -> B1 -> B2 -> A2 | None, None |

At each comparison, the smaller head is no larger than anything in either remaining sorted
suffix. Appending it preserves sorted order. Save or advance the selected input cursor and
advance tail to the selected object. Only the prefix through tail is committed; tail.next
may still point into an unconsumed suffix until the next splice. When one input is exhausted,
attach the other whole suffix because it is sorted and follows the last selected value.

Every original node enters the committed output exactly once. With disjoint inputs this
prevents loss, duplication, and cycles. The iterative merge uses O(n+m) time in the worst
case and O(1) workspace; construction and serialized output each use O(n+m) storage locally.
A recursive version consumes stack space and does not meet constant-workspace reasoning.
Concatenating values and sorting is a simple value oracle, but does not satisfy relinking.

On equality either list may be selected for the numeric contract; choosing left consistently
also preserves left-before-right order among equal cross-list values. For both empty inputs,
dummy.next remains None. If only one is empty, attach the nonempty head immediately.
Online receives two heads and returns a head; locally build from a/b and serialize afterward.
Inspect original identities as well as values when testing the relinking requirement.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
class Node:
    def __init__(self, value, next=None):
        self.value, self.next = value, next

a, b = Node(2), Node(5)
copied = Node(a.value, Node(b.value))
print('copied values:', copied.value, copied.next.value)
print('preserves identity:', copied is a)
assert copied is not a
dummy = Node(None)
tail = dummy
tail.next = a
tail = a
tail.next = b
print('relinked:', dummy.next is a, a.next is b)
assert dummy.next is a and a.next is b and b.next is None
```

**Line by line:** The copied chain matches values while failing identity. A dummy and tail then demonstrate two splices using the original objects. The assertions check ownership of nodes; serialization alone cannot distinguish these implementations.

Observed author output on Python 3.12.10, 2026-09-23:

```text
copied values: 2 5
preserves identity: False
relinked: True True
```

These are author teaching observations. The deterministic models do not measure production
performance or prove the behavior of a deployed cache or concurrent service.

## In production

Relinking consumes the input topology: callers must permit that mutation. Shared suffixes
violate the disjointness assumption and can produce a self-loop when the same object is
selected twice. If sharing is allowed, change the contract and algorithm or copy deliberately;
do not silently apply a proof for disjoint lists.

## Check yourself

### Readiness before practice

1. Why can you attach the whole remainder without more comparisons?
2. Which pointer must move after attaching a selected node?
3. How can an output-value test pass while the relinking requirement fails?

Return to [README.md](README.md) for the assignment, verification, and evidence route.
Keep the independent 60/30/15-minute budgets; extra depth can wait for another sitting.
