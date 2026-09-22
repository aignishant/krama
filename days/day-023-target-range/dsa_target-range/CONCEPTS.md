---
day: 23
part: "1.1"
title: "Find a run with two boundaries"
ids: [DSA-23]
level: working
prerequisites: ["Day 22 lower-bound invariant"]
failure: true
---

# Find a run with two boundaries

Core reading: explanation, worked trace, and readiness within the existing track cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Find the first value >= target and the first value > target; the equal run lies between those boundaries.

## The story

A log groups equal timestamps together. One equality match says nothing about how many adjacent records share that timestamp.

## The idea in plain language

Start with [Day 22](../../day-022-lower-bound/dsa_lower-bound/CONCEPTS.md).
Lower bound L is the first index with value >= target; upper bound U is the first with value
> target. Sorted order makes all target occurrences contiguous. Their half-open range is
[L,U), length U-L. The requested output instead uses inclusive endpoints, [L,U-1], and
[-1,-1] when absent. A boundary alone does not certify that the target exists.

## Why Krama needs it

This develops DSA-23 in its independent track. Use the prerequisite named above;
the other two tracks are not prerequisites. The [day hub](../LESSON.md) preserves the daily budgets.

## The source behind it

[Python bisect](https://docs.python.org/3.12/library/bisect.html) defines both partitions; [LeetCode 34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) supplies the companion output contract.
Source links checked 2026-09-22; see [the source ledger](../../../docs/SOURCES.md).
The examples and small failure models below are original teaching demonstrations.

## The mechanism

### Worked trace

For [1, 3, 3, 3, 8, 10] and target 3, both searches start with lo=0 and hi=6:

| Search | mid and decision sequence | Final boundary |
| --- | --- | --- |
| First >=3 | 3 qualifies → hi=3; 1 qualifies → hi=1; 0 too small → lo=1 | L=1 |
| First >3 | 3 equal → lo=4; 5 greater → hi=5; 4 greater → hi=4 | U=4 |

Thus the result is [1,3] and there are three matches. For target 4, both boundaries equal
4, but nums[4] is 8: return [-1,-1]. Before reading nums[L], check L<n. An equivalent
absence test is L==U when both correct boundary searches have already run.

Lower search preserves the Day 22 partition. Upper search treats equality as too far left,
so its false region contains all values <= target. Combining the partitions proves that
exactly the positions from L through U-1 equal target. Both intervals shrink independently.
Two O(log n) searches still take O(log n) time and O(1) auxiliary/output space. Finding one
match and walking outward costs O(n) on an all-equal array. A full scan is a useful baseline
but cannot justify the requested logarithmic worst-case bound.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
from bisect import bisect_left, bisect_right

def endpoints(values, target):
    left = bisect_left(values, target)
    if left == len(values) or values[left] != target:
        return [-1, -1]
    return [left, bisect_right(values, target) - 1]

values = [1, 3, 3, 3, 8, 10]
wrong = [bisect_left(values, 4), bisect_right(values, 4) - 1]
print('unchecked absence:', wrong, 'checked:', endpoints(values, 4))
assert wrong == [4, 3]
assert endpoints(values, 3) == [1, 3]
assert endpoints([], 3) == [-1, -1]
assert endpoints([3, 3, 3], 3) == [0, 2]
print('inclusive endpoints:', endpoints(values, 3))
```

**Line by line:** The library functions expose the two boundaries without filling your exercise. Subtracting one before checking absence creates an inverted range. The repaired adapter distinguishes absent, empty, and all-equal inputs.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
unchecked absence: [4, 3] checked: [-1, -1]
inclusive endpoints: [1, 3]
```

The failing behavior is deliberate; subsequent assertions check the repair on these examples.
An executed Python model does not establish database behavior or production performance.

## In production

Keep boundary semantics explicit in APIs: [L,U) composes cleanly with slicing, but this
exercise requests an inclusive last index. Prefer a direct > predicate to searching for
target+1; the latter assumes a discrete successor and can overflow in fixed-width languages.
Optional depth: count occurrences with U-L without materializing the matching slice.

## Check yourself

### Readiness before practice

1. Why are equal values one contiguous run?
2. Which inequality changes between the two searches?
3. What does L=U mean, and why is [L,U-1] then the wrong public result?
4. Why does expansion from one match lose the logarithmic guarantee?

Use [README.md](README.md) for the assignment, verification, and personal evidence route.
Reading the lesson does not complete study.
