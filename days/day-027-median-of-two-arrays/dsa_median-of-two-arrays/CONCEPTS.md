---
day: 27
part: "1.1"
title: "Median of two arrays"
ids: [DSA-27]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Median of two arrays

Core reading: intuition, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting. Record partial progress if needed.

## One-line answer

Partition two sorted arrays into balanced halves whose cross-boundaries are ordered; the median sits at the cut.

## The story

Two sorted stacks of receipts contain one combined middle price. Merging every receipt works, but you only need to know what lies immediately beside the combined middle.

## The idea in plain language

Begin with [merging sorted inputs](../../day-005-merge-sorted-arrays/dsa_merge-sorted-arrays/CONCEPTS.md)
and [lower bound](../../day-022-lower-bound/dsa_lower-bound/CONCEPTS.md). A partition cuts an array
between elements. For odd total length, the left half should contain one extra item; for even
length, the halves have equal sizes. A valid partition puts every left value before every right
value. Sorting within each array is already guaranteed, so only two cross-array comparisons
need checking. This is the core mechanism for both the local and online routes, not an extra
optional problem.

## Why Krama needs it

This develops DSA-27 independently of the other two tracks. The [day hub](../LESSON.md)
links the separate 60/30/15-minute routes; completing the reading is not passing the assignment.

## The source behind it

[Median of Two Sorted Arrays, LeetCode 4](https://leetcode.com/problems/median-of-two-sorted-arrays/) specifies sorted inputs, a nonempty combined input, and logarithmic runtime.
Checked 2026-09-23; details are in the [source ledger](../../../docs/SOURCES.md).
The traces, examples, and failure demonstrations here are original teaching material.

## The mechanism

### Worked trace

First derive a baseline: merge until the middle, remembering the last two emitted values.
This takes O(m+n) time and O(1) extra space without constructing the merged array. Keep it as a
small-case oracle. For the logarithmic method, name the shorter array A (length m) and the other
B (length n). Let h=(m+n+1)//2. Choose i left-side items from A; then j=h-i must come from B.
Searching 0<=i<=m keeps j in [0,n] because m<=n.

Define AL=A[i-1], AR=A[i], BL=B[j-1], BR=B[j]. At empty left boundaries use conceptual -infinity;
at empty right boundaries use +infinity. No out-of-range read should occur.

For A=[2,8], B=[1,3,7,9], h=3:

| i | j | Left halves | Right halves | Cross checks |
| --- | --- | --- | --- | --- |
| 1 | 2 | [2] and [1,3] | [8] and [7,9] | 2<=7 and 3<=8 |

Both hold, so the middle two values are max(2,3)=3 and min(8,7)=7; median=5.
For A=[8,9], B=[1,2,3,4], the initial i=1 gives AL=8>BR=3: too many large A items
are on the left. Decrease i. At i=0, j=3, the cut works and median=(3+4)/2=3.5.

If AL>BR, moving i farther right only increases AL and moves BR left toward smaller values;
discard i and every larger cut. If BL>AR, moving i left makes that violation no better;
discard i and every smaller cut. Otherwise both cross checks hold. Internal sorting plus
these comparisons proves the entire left half is <= the entire right half. Equal values are
allowed, so comparisons are non-strict. A stable tie ordering is unnecessary.

For odd total length return the largest left value; for even length average the largest left
and smallest right. One empty array is valid; two empty arrays violate the contract. The search
uses O(1+log(min(m,n)+1)) time and O(1) extra space with constant-time indexed numeric comparisons.
Swapping references is constant space; copying or slicing arrays is not. Implement boundaries
with explicit cases if the value type has no suitable infinity sentinel.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
a = [1, 2]
b = [10, 11]
i, j = 2, 0
al, ar = a[i - 1], float("inf")
bl, br = float("-inf"), b[j]
left_middle = max(al, bl)
wrong = left_middle
right = (left_middle + min(ar, br)) / 2
print("left maximum only:", wrong, "even-length median:", right)
assert al <= br and bl <= ar
assert wrong != 6
assert right == 6
print("ordered cut and even-length rule checked")
```

**Line by line:** This checks one given cut rather than solving the search. The infinity values represent absent neighbors. The two cross checks certify the cut, while the final assertions isolate the separate mistake of returning only one middle value for an even total.

Observed author output on Python 3.12.10, 2026-09-23:

```text
left maximum only: 2 even-length median: 6.0
ordered cut and even-length rule checked
```

The deliberate failure and repaired assertions are teaching evidence, not learner progress.
Python state models do not demonstrate PostgreSQL isolation or production performance.

## In production

A reviewer should reject binary search that validates ordering by sorting first: it loses the
target cost and silently changes the input contract. Numeric NaN values do not provide the
ordering assumed by the proof. Arbitrarily large integer medians may need an exact rational
representation in application code. This is a stretch day: derive the baseline and invariant
within the hour, then record partial progress if the partition search needs another sitting.

## Check yourself

### Readiness before practice

1. Why is searching the shorter array necessary for the simple cut bounds?
2. Explain the direction change when AL>BR without quoting a template.
3. Trace one empty array and two arrays containing only the same value.
4. Why does total parity change how the boundary values are used?

Run the teaching block only if you need to check your prediction. Then return to
[README.md](README.md) for the assignment, verification, and personal evidence route.
