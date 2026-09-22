---
day: 3
part: "1.1"
title: "Build a stable prefix without overwriting unread input"
ids: [DSA-03]
level: working
prerequisites: ["Scan invariants", "List mutation"]
failure: true
---

# Build a stable prefix without overwriting unread input

Core for both practice routes. Read the trace and readiness questions before implementing;
the optional discussion about fewer writes can wait until review.

## One-line answer

Separate the position being read from the next position where a retained item belongs.

## The story

You tidy a row of appointment cards by removing cancelled slots. The remaining appointments
must keep their order. Moving the last card into the first gap fills the gap quickly, but may
put a late appointment before an early one. Instead, move cards forward in their original order.

## The idea in plain language

**Stable** means retained items keep their relative order. **Compaction** packs retained items
into a prefix. Recall [the invariant proof structure](../../day-001-count-target-values/dsa_count-target-values/CONCEPTS.md).
This pattern fits filtering inside an existing array when extra storage is constrained. A
separate result list is a simple O(n)-space baseline; deleting each unwanted element can shift
the remaining suffix repeatedly, creating quadratic work.

## Why Krama needs it

You now have two moving positions with different meanings. The safety condition between them
explains why mutation can be correct even while reading the same list.

## The source behind it

[Move Zeroes](https://leetcode.com/problems/move-zeroes/), checked 2026-09-22, requires a stable
result in the input array. Its judge observes mutation. The local adapter also returns that
modified list. See `spec:leetcode-283` in [sources](../../../docs/SOURCES.md).

## The mechanism

### Worked trace

Teaching cards: `["A", None, "B", None, "C"]`; `None` marks an empty slot. Let read inspect
each original position and write count the retained cards already placed.

| Read index | Value seen | Action | Write afterwards | Valid prefix afterwards |
| --- | --- | --- | --- | --- |
| 0 | A | Place at 0 | 1 | A |
| 1 | empty | Skip | 1 | A |
| 2 | B | Place at 1 | 2 | A, B |
| 3 | empty | Skip | 2 | A, B |
| 4 | C | Place at 2 | 3 | A, B, C |

Before each read, positions below write contain exactly the retained items from the already
read prefix, in their original order. Initially that prefix is empty. A skipped item changes
neither contents nor write. A retained item is appended to the valid prefix and write advances.
Because write ≤ read, its destination is never an unread future position. This proves safety
as well as order preservation.

After the scan, the prefix is correct but the tail can still contain old values. Fill positions
write through n−1 with the required empty marker only **after** reading finishes. The final
count of empty slots is n−write. For the assignment, zero is the marker; negative numbers are
retained too. The tail is not required to be valid during the scan.

### Cost and ownership

One read pass and at most one tail pass use O(n) time, O(1) auxiliary space, and preserve list
length and identity. Returning the same list does not allocate another O(n) result. Returning
an equal new list fails the local mutation promise. Empty input naturally needs no writes;
the online problem specifies nonempty input. All-empty and no-empty inputs test both extremes.

## When it breaks

A quick swap with the last card breaks stability even though it removes the leading gap.

```python
cards = [None, "A", "B"]
cards[0], cards[2] = cards[2], cards[0]
print("end swap:", cards)
try:
    assert cards[:2] == ["A", "B"], "retained cards changed order"
except AssertionError as error:
    print(f"AssertionError: {error}")

cards = [None, "A", "B"]
write = 0
for read in range(len(cards)):
    if cards[read] is not None:
        cards[write] = cards[read]
        write += 1
for index in range(write, len(cards)):
    cards[index] = None
assert cards == ["A", "B", None]
print("stable packing:", cards)
```

**Line by line:** the swap moves B ahead of A, and the assertion tests ordering rather than
merely membership. The repaired demonstration resets the fixture, reads each position, writes
only retained cards, then clears the stale tail. `is not None` tests this example's empty-slot
marker; choose the predicate required by your own problem. Slices in the diagnostic assertion
allocate memory; they are not part of the constant-space compaction algorithm.

Author verification on Python 3.12.10, 2026-09-22:

```text
end swap: ['B', 'A', None]
AssertionError: retained cards changed order
stable packing: ['A', 'B', None]
```

## In production

Stable filtering matters when event order encodes meaning. An unordered partition can be a
valid alternative only when the API allows it. In-place mutation also means aliases observe
changes; callers needing the original data require a different ownership contract. Optional:
avoid assigning an item to its own position to reduce writes, but prove correctness first.

## Check yourself

### Readiness before practice

1. Why can write lag behind read, but never lead it?
2. What stale values remain before tail cleanup for `[None, "A", "B"]`?
3. Why does `[0, -3, 0, 2]` retain −3?
4. How would you detect a solution that returns the right values in a new list?

Then choose [local practice](PRACTICE.md) or [LeetCode](LEETCODE.md). Locally run
`python course.py practice 3` after your implementation. Test ordering, length, list identity,
all-zero, no-zero, and alternating inputs; fixture equality alone does not prove mutation.
Record your own failure and repair in [NOTES.md](NOTES.md).

[Navigation](README.md) · [Quick recall](../../../docs/DSA_RECALL.md#day-003-stable-compaction)
