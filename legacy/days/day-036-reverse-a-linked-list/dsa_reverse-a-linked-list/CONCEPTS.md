---
day: 36
part: "1.1"
title: "Reverse a linked list"
ids: [DSA-36]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Reverse a linked list

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Reverse a singly linked list by saving the next node before redirecting each link toward the processed prefix.

## The story

You redirect the first link in a chain and then try to follow it forward. The remaining nodes are no longer reachable through that link.

## The idea in plain language

Recall [mutation contracts](../../day-006-best-single-trade/lang_mutation-contracts/CONCEPTS.md) if object aliasing is unfamiliar; this DSA
lesson otherwise stands alone. A singly linked node stores a value and one reference called
next. The head is a reference to the first node; None ends the chain. Reversal changes those
references, preserving node identity and values. Reversing only an array of values evades the
local assignment, which requires real nodes, link reversal, and serialization.

## Why Krama needs it

This develops DSA-36. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Official LeetCode companion](https://leetcode.com/problems/reverse-linked-list/) defines the online contract; [LEETCODE.md](LEETCODE.md) compares it with local practice.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

For A -> B -> C -> None, keep prev=None and curr=A.

| Step | Save before changing | Reverse link | Move state |
| --- | --- | --- | --- |
| 1 | next=B | A.next=None | prev=A, curr=B |
| 2 | next=C | B.next=A | prev=B, curr=C |
| 3 | next=None | C.next=B | prev=C, curr=None |

The invariant is two disjoint chains: prev heads the reversed processed prefix, and curr
heads the untouched suffix. Saving curr.next keeps the suffix reachable while changing the
current edge. Each iteration transfers exactly one node, so it terminates after n nodes.
When curr is None, prev heads the full reversed list. Empty input keeps prev=None; a singleton
keeps the same node with next=None. This reasoning assumes an acyclic finite input list.

Pointer reversal takes O(n) time and O(1) auxiliary state. The local adapter still allocates
O(n) nodes when building and O(n) values when serializing. A recursive reversal uses O(n)
call stack and can hit Python's recursion limit; it is not constant-space. Online receives
an existing head and returns a head, whereas local solve returns a JSON-compatible value list.
Check node identities and absence of cycles as well as serialized values in your own tests.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
class Node:
    def __init__(self, value, next=None):
        self.value, self.next = value, next

b = Node('B')
a = Node('A', b)
a.next = None  # Bug: suffix was not saved before overwriting.
print('wrong next reachable:', a.next)
assert a.next is None  # b survives only through our separate test reference.
a.next = b
saved = a.next
a.next = None
b.next = a
print('repaired chain:', b.value, b.next.value, b.next.next)
assert saved is b and b.next is a and a.next is None
```

**Line by line:** The test holds a separate b reference so it can demonstrate and repair the lost forward path. Saving next before rewriting preserves the suffix. The final identity checks verify that original nodes are relinked rather than replaced with copied values.

Observed author output on Python 3.12.10, 2026-09-23:

```text
wrong next reachable: None
repaired chain: B A None
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Callers holding node references observe changed links; document exclusive mutation ownership.
Concurrent readers cannot safely traverse a list while these links are reversed without an
appropriate synchronization contract. Reject or separately handle cycles rather than assuming
the loop must finish. A reviewer should ask whether the container representation is appropriate:
Python lists often fit application workloads better than hand-built linked structures.

## Check yourself

### Readiness before practice

1. Which reference is lost if curr.next is overwritten first?
2. What does prev mean after two steps?
3. Why can the core use O(1) space while the local adapter uses O(n)?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.
