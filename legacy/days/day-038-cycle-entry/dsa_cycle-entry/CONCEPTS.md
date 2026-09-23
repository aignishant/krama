---
day: 38
part: "1.1"
title: "Cycle entry"
ids: [DSA-38]
level: working
prerequisites: ["See the linked prerequisite explanation below"]
prev: README.md
next: README.md
failure: true
---

# Cycle entry

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Detect a meeting using unequal speeds, then walk from the head and meeting node at equal speeds to find the cycle entry.

## The story

Two tasks have the same label, but they are different nodes. A repeated label is harmless; returning to the same object is the cycle.

## The idea in plain language

Start with [the slow/fast distance model](../../day-037-middle-node/dsa_middle-node/CONCEPTS.md).
A cycle is a repeated node identity when following next. Its entry is the first cyclic node
reachable from the head. Use this technique when a chain may revisit objects and memory is
constrained. The chain consists of a noncyclic prefix of length mu and a loop of length lam.

## Why Krama needs it

This develops DSA-38; the [day hub](../LESSON.md) keeps the tracks independent.
Use the explanation to reason before practice. Reading does not establish study completion.

## The source behind it

[Official LeetCode problem](https://leetcode.com/problems/linked-list-cycle-ii/) supplies the online contract; [LEETCODE.md](LEETCODE.md) compares its interface with local practice.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The worked examples, proofs, and numeric scenarios below are original teaching material.

## The mechanism

### Worked trace

Trace A -> B -> C -> D -> E -> C, so mu=2 and lam=3. Compare identities after each advance:

| Round | slow | fast |
| --- | --- | --- |
| 0 | A | A (initial equality is not detection) |
| 1 | B | C |
| 2 | C | E |
| 3 | D | D (meeting) |

Once both are in the loop, fast gains one position per round modulo lam, so a meeting must
occur within lam more rounds. If fast or its next is None first, the chain has no cycle.
At the meeting, slow has walked t edges, fast 2t; their difference t is a multiple of lam.
The meeting is at offset (t-mu) modulo lam from entry. Walking mu more steps from there
therefore reaches offset t modulo lam = 0, the entry.

Reset one pointer to A, leave the other at D, then advance both one edge: (A,D), (B,E),
(C,C). Before the first pointer reaches C it is outside the loop, so they cannot meet earlier.
If mu=0, the meeting node is already the head and the reset phase takes zero steps.

A visited-identity map is an easier O(L)-space baseline: the first node revisited is entry.
Floyd's method takes O(mu+lam) time and O(1) detection space, without modifying links.
Use `is`, not payload equality or recursive structural equality. A plain Node class avoids
accidentally generating recursive comparisons for a cyclic graph.

Local `pos` is input-adapter metadata: use it once to connect the constructed tail, then
detect from the head without consulting it. After detection, a bounded head-to-entry walk
can recover the zero-based index. Do not serialize by walking until None on a cycle.
The online task receives only head and returns an entry node or None; pos is not an algorithm
parameter. The local result is an index or -1. Node construction still uses O(L) memory.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
class Node:
    def __init__(self, value, next=None):
        self.value, self.next = value, next

b = Node(7)
a = Node(7, b)
print('payload claims cycle:', a.value == b.value)
print('same node:', a is b)
assert a.value == b.value and a is not b and b.next is None
nodes = [Node(letter) for letter in 'ABCDE']
for left, right in zip(nodes, nodes[1:]):
    left.next = right
nodes[-1].next = nodes[2]
slow = fast = nodes[0]
for step in range(1, 4):
    slow, fast = slow.next, fast.next.next
    print(step, slow.value, fast.value)
assert slow is fast is nodes[3]
left, right = nodes[0], slow
while left is not right:
    left, right = left.next, right.next
print('entry:', left.value)
assert left is nodes[2]
```

**Line by line:** The first chain disproves value-based detection. Five separately allocated objects then create the traced loop. Three rounds reach D; resetting one pointer and using identity finds C. The fixed three-round loop illustrates this particular topology, not a general detection implementation.

Observed author output on Python 3.12.10, 2026-09-23:

```text
payload claims cycle: True
same node: False
1 B C
2 C E
3 D D
entry: C
```

These are author teaching observations. The deterministic models do not measure production
performance or prove the behavior of a deployed cache or concurrent service.

## In production

Test an empty list, an acyclic singleton, a self-loop, entry at head, a long prefix, and
repeated payload values. Graph debugging and cleanup need bounded traversal too: even a
logging helper can hang if it assumes every next chain ends. No traversal guarantee survives
arbitrary simultaneous mutation.

## Check yourself

### Readiness before practice

1. Why must the first phase advance before treating equality as a meeting?
2. In the trace, why is D a meeting but C the entry?
3. Which part of the memory claim excludes local node construction?

Return to [README.md](README.md) for the assignment, verification, and evidence route.
Keep the independent 60/30/15-minute budgets; extra depth can wait for another sitting.
