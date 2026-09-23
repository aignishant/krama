---
day: 5
part: "1.2"
title: "Use spare capacity without destroying unread values"
ids: [DSA-05]
level: working
prerequisites: ["Two-head merge", "Mutation and pointer invariants"]
failure: true
---

# Use spare capacity without destroying unread values

Read after [the main merging lesson](CONCEPTS.md). Required preparation for the online route;
optional for the local new-output route. This changes where you write and which candidates you choose.

## One-line answer

When spare output capacity is at the end of an input array, finalize the largest remaining values from right to left.

## The story

One desk's appointment row has spare slots at the right, and another desk sends more cards.
Putting an early incoming appointment into the leftmost slot can erase a card still waiting
to be read. Placing the latest appointment into the last free slot avoids that collision.

## The idea in plain language

A **logical length** counts meaningful items; physical list length includes spare positions.
Treat lengths as authoritative. A zero in a meaningful position is data, while a zero beyond
the logical end is merely a placeholder. Removing every zero confuses those two roles.

## Why Krama needs it

The local exercise allocates a new list. The online exercise writes into an existing array.
Choosing a scan direction is now an ownership and safety decision, not just a stylistic choice.

## The source behind it

[88. Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/), checked 2026-09-22,
provides `nums1` with m valid values followed by n spare slots, and `nums2` with n values.
Its result belongs in `nums1`; a newly returned list does not satisfy the interface. Either
logical input may be empty, but the combined length is positive. See `spec:leetcode-88` in
[the source ledger](../../../docs/SOURCES.md).

## The mechanism

### Worked trace

Let the destination be `[2, 8, 0, 0]` with two meaningful values; incoming values are `[3, 9]`.
Use i=m−1 and j=n−1 for the last unread values and k=m+n−1 for the next destination slot.

| Candidates | Write | Destination afterwards | New i, j, k |
| --- | --- | --- | --- |
| 8 and 9 | 9 at 3 | 2, 8, 0, 9 | 1, 0, 2 |
| 8 and 3 | 8 at 2 | 2, 8, 8, 9 | 0, 0, 1 |
| 2 and 3 | 3 at 1 | 2, 3, 8, 9 | 0, −1, 0 |
| Incoming exhausted | Leave remaining 2 in place | 2, 3, 8, 9 | Done |

At each step the suffix after k is final. Sorted inputs make the larger unread tail the
largest remaining value, so it belongs at k. Advance backward only in the source selected,
then decrement k. While incoming items remain, `k = i + j + 1`, hence k>i; writing at k cannot
overwrite unread destination data. The incoming array is separate storage.

If incoming runs out, k=i and the remaining destination prefix is already correctly placed.
If destination data runs out first, copy the remaining incoming values into the open positions.
Never read index −1 as a substitute for an exhausted input: Python treats it as a valid index
into a nonempty list. Check exhaustion before comparing.

Each write finalizes one position, giving O(m+n) time and O(1) auxiliary space with no new
result array. The supplied capacity is part of the input, not newly allocated working memory.
Optional stability: for equal keys, taking from the second input when filling backward places
its record later, preserving first-input-before-second-input order in the final array.

## When it breaks

This small demonstration isolates the overwrite hazard before introducing a complete loop.

```python
row = [5, 8, None]
incoming = 2
row[0] = incoming
print("forward overwrite:", row)
try:
    assert 5 in row, "an unread destination value was overwritten"
except AssertionError as error:
    print(f"AssertionError: {error}")

row = [5, 8, None]
row[2] = row[1]
row[1] = row[0]
row[0] = incoming
assert row == [2, 5, 8]
print("fill from the back:", row)
```

**Line by line:** the first write destroys 5 before it can be consumed. Resetting the fixture
restores the data. Copying 8 rightward first frees its old position; copying 5 into that position
frees slot zero for 2. `None` makes this teaching fixture's capacity visible; the online buffer
uses zeros, whose meaning is determined by m. Your own implementation must generalize the trace.

Author verification on Python 3.12.10, 2026-09-22:

```text
forward overwrite: [2, 8, None]
AssertionError: an unread destination value was overwritten
fill from the back: [2, 5, 8]
```

## In production

Before writing into a reused buffer, document capacity, valid length, overlap, and ownership.
This proof depends on separate incoming storage and spare tail capacity. It does not solve
merging two arbitrary adjacent arrays without spare room. Allocating a new destination remains
a simpler valid choice when the API permits its memory cost.

## Check yourself

### Readiness before practice

Explain why `[0, 4, 0]` with m=2 contains a real zero. Why is a remaining destination prefix
already in place when j becomes −1? Trace m=0 and n=0 separately. Which direction is safe if
the spare capacity is at the right, and what inequality proves it?

Continue to [LeetCode practice](LEETCODE.md). Include valid zeros, all incoming values smaller,
all incoming values larger, duplicates, and one logically empty input. Record actual submission
evidence and the local/online contract difference in [NOTES.md](NOTES.md).

[Main lesson](CONCEPTS.md) · [Navigation](README.md)
