---
day: 37
part: "1.1"
title: "Middle node"
ids: [DSA-37]
level: working
prerequisites: ["See the linked prerequisite explanation below"]
prev: README.md
next: README.md
failure: true
---

# Middle node

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Move one pointer once and another twice per round; when the faster one finishes, the slower one is at the second middle.

## The story

A queue is a chain of nodes with no stored length. Counting works, but finding its midpoint need not require a second walk.

## The idea in plain language

Recall [node references and link traversal](../../day-036-reverse-a-linked-list/dsa_reverse-a-linked-list/CONCEPTS.md).
A node is an object, its value is payload, and next is an edge to another object or None.
Use relative pointer speeds when a position is defined as a fraction of an unknown chain length.
Both pointers start at the head. This assumes a finite acyclic chain and leaves its links untouched.

## Why Krama needs it

This develops DSA-37; the [day hub](../LESSON.md) keeps the tracks independent.
Use the explanation to reason before practice. Reading does not establish study completion.

## The source behind it

[Official LeetCode problem](https://leetcode.com/problems/middle-of-the-linked-list/) supplies the online contract; [LEETCODE.md](LEETCODE.md) compares its interface with local practice.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The worked examples, proofs, and numeric scenarios below are original teaching material.

## The mechanism

### Worked trace

For A -> B -> C -> D -> E -> F -> None, the pointers occupy:

| Completed rounds | slow | fast |
| --- | --- | --- |
| 0 | A | A |
| 1 | B | C |
| 2 | C | E |
| 3 | D | None |

Before advancing twice, check `fast is not None and fast.next is not None` in that order.
After k rounds slow has advanced k edges and fast has advanced 2k. For length 2m, fast
reaches None after m rounds, leaving slow at index m, the second middle. For length 2m+1,
fast reaches the last node after m rounds, again leaving slow at index m. Empty input starts
with both None; return None without reading a value. A singleton takes zero rounds.

A two-pass baseline counts L nodes then walks L//2 edges; it is also O(L) time and O(1)
traversal space. The speed technique reduces passes, not the asymptotic bound. Building local
nodes costs O(L) space even though the traversal retains only two references. A list of all
node references is another valid baseline but requires O(L) extra traversal memory.

The online answer is the middle **node**, not its value or a copied suffix. Local practice
builds nodes from `values` and returns only the middle value, with None for empty input;
the online constraints are nonempty. Do not treat the online display of a suffix as an array
return requirement. The loop guard chooses the tie rule: stopping one round sooner on an even
chain gives the first middle instead.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
class Node:
    def __init__(self, value, next=None):
        self.value, self.next = value, next

b = Node('B')
a = Node('A', b)
slow = fast = a
# Wrong guard for the SECOND-middle contract.
while fast.next is not None and fast.next.next is not None:
    slow, fast = slow.next, fast.next.next
print('wrong middle:', slow.value)
assert slow is a
slow = fast = a
while fast is not None and fast.next is not None:
    slow, fast = slow.next, fast.next.next
print('second middle:', slow.value)
assert slow is b and a.next is b
```

**Line by line:** The first two objects form an even chain. The wrong guard requires two real successor nodes and skips the needed round. The corrected guard allows fast to land on None. Identity assertions distinguish the actual returned node and confirm no relinking.

Observed author output on Python 3.12.10, 2026-09-23:

```text
wrong middle: A
second middle: B
```

These are author teaching observations. The deterministic models do not measure production
performance or prove the behavior of a deployed cache or concurrent service.

## In production

A cycle invalidates the stopping argument; use the next lesson's cycle handling if inputs
can be cyclic. Concurrent link edits also invalidate the distance relationship. Keep node
construction and traversal costs separate when reviewing a benchmark or interview explanation.

## Check yourself

### Readiness before practice

1. Where do the pointers stop on five nodes and on six?
2. Why is `fast.next` unsafe to inspect before checking fast?
3. Which resource cost changes if you collect every node in an array?

Return to [README.md](README.md) for the assignment, verification, and evidence route.
Keep the independent 60/30/15-minute budgets; extra depth can wait for another sitting.
