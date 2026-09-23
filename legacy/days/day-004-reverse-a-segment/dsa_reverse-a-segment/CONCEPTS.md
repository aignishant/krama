---
day: 4
part: "1.1"
title: "Finalize mirrored pairs from the outside inward"
ids: [DSA-04]
level: working
prerequisites: ["Scan invariants", "List mutation and indices"]
failure: true
---

# Finalize mirrored pairs from the outside inward

Read this core explanation before either route. Optional variations belong in spare time or
a later review; the main attempt stays within the existing DSA hour.

## One-line answer

Swap mirrored endpoints, then shrink the unfinished interval until fewer than two positions remain.

## The story

You reverse a row of labelled cards on a desk. The first card belongs in the last position,
and the last belongs in the first. Once you exchange those two, both are finished. There is
no reason to touch them again while reversing the cards between them.

## The idea in plain language

A **closed interval** `[L, R]` includes both endpoints and contains R−L+1 positions. For an
original position i in that interval, reversal sends its value to L+R−i. This symmetry suggests
two pointers approaching each other. It differs from Day 3: neither pointer scans ahead to
filter; each step finalizes two positions.

Recall [invariants](../../day-001-count-target-values/dsa_count-target-values/CONCEPTS.md).
Keep the original interval fixed in the proof even as the working pointers move. Positions
outside the original interval must remain unchanged.

## Why Krama needs it

Pointer algorithms become easier to reason about when you can identify which positions are
finished and how much unfinished work remains. Today the unfinished interval shrinks by two.

## The source behind it

[Reverse String](https://leetcode.com/problems/reverse-string/), checked 2026-09-22, applies this
idea to a whole character array with constant extra memory. The local task instead specifies
an inclusive integer subrange and returns the modified list. See `spec:leetcode-344` in
[sources](../../../docs/SOURCES.md).

## The mechanism

### Worked trace

For cards `["X", "A", "B", "C", "D", "Y"]`, reverse the closed interval `[1, 4]`.

| Step | Left, right | Exchange | Array afterwards |
| --- | --- | --- | --- |
| Start | 1, 4 | Nothing yet | X, A, B, C, D, Y |
| First pair | 1, 4 | A with D | X, D, B, C, A, Y |
| Second pair | 2, 3 | B with C | X, D, C, B, A, Y |
| Stop | 3, 2 | Pointers have crossed | X, D, C, B, A, Y |

Before each swap, every position in the original interval but outside the working pointers
already contains its final value. Initially there are no such positions. Swapping endpoints
puts both mirrored values in their final locations; advancing left and retreating right
preserves the invariant. The number of unfinished positions decreases, so the process ends.
An odd-length interval leaves one middle item, whose mirror is itself. A singleton needs no swap.

Let k=R−L+1. There are floor(k/2) swaps: O(k) time, O(1) auxiliary space. Returning the existing
list adds no new result allocation. A reversed slice is a convenient O(k)-space baseline,
but it cannot support a constant-extra-space claim. Reversing a slice object alone also leaves
the original list unchanged unless the result is assigned back.

The local precondition is `0 <= left <= right < n`; an empty list is outside that contract.
Do not invent a required behavior for invalid ranges. Define a separate contract if exploring them.

## When it breaks

Sequential overwrites lose the old left value before the right side can receive it.

```python
cards = ["A", "B"]
cards[0] = cards[1]
cards[1] = cards[0]
print("overwritten:", cards)
try:
    assert cards == ["B", "A"], "the original left card was lost"
except AssertionError as error:
    print(f"AssertionError: {error}")
cards = ["A", "B"]
saved = cards[0]
cards[0] = cards[1]
cards[1] = saved
assert cards == ["B", "A"]
print("saved swap:", cards)
```

**Line by line:** the first assignment destroys access to A through the list. Reading index
zero on the next line now yields B. The repair saves a reference before either write, so each
old value remains available. Python's simultaneous assignment is another way to express a
swap, but understanding the saved value explains why two sequential writes are insufficient.

Author verification on Python 3.12.10, 2026-09-22:

```text
overwritten: ['B', 'B']
AssertionError: the original left card was lost
saved swap: ['B', 'A']
```

An additional failure is swapping every original index with its mirror: that visits each pair
twice and undoes the reversal. Stop when the pointers meet or cross.

## In production

Review interval conventions before optimizing a buffer operation: many APIs use an exclusive
end, whereas this exercise includes it. Test untouched prefix and suffix values, not just the
reversed region. Whole-string reversal here means array positions; extending it to human text
requires defining a text unit, because reversing code points need not preserve displayed symbols.
That extension is optional and outside this character-array assignment.

## Check yourself

### Readiness before practice

1. In `[L, R]=[2, 6]`, where does original position 3 belong?
2. Why does the middle position of an odd interval need no write?
3. Which assertions distinguish a whole-list reversal from the requested subrange reversal?
4. Why is reversing twice useful but insufficient alone? Consider a function that does nothing.

Open [local practice](PRACTICE.md) or [LeetCode practice](LEETCODE.md), then implement on your
own. Locally run `python course.py practice 4`. Add singleton, two-item, odd/even, repeated-value,
and interior-subrange checks as appropriate. Verify identity and outside-region preservation.
Use reversal-twice as an extra property alongside independently calculated expected output.
Record evidence in [NOTES.md](NOTES.md).

[Navigation](README.md) · [Quick recall](../../../docs/DSA_RECALL.md#day-004-reverse-a-segment)
