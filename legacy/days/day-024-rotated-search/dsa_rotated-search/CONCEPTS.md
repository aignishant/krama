---
day: 24
part: "1.1"
title: "Search the sorted half of a rotation"
ids: [DSA-24]
level: working
prerequisites: ["Day 22 shrinking search intervals; strict sorted order"]
failure: true
---

# Search the sorted half of a rotation

Core reading: explanation, worked trace, and readiness within the existing track cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

After checking the midpoint, identify a sorted half and keep it only if its value range contains the target.

## The story

A sorted inventory was rotated when its circular buffer wrapped. Ordinary binary search discards the wrong half because the whole visible list is no longer sorted.

## The idea in plain language

A rotation of a strictly increasing array has at most one descending seam. Therefore at
least one half adjacent to the midpoint is sorted. Use an inclusive candidate interval
[lo,hi], unlike Day 22's half-open boundary search. The invariant is that an existing target
remains inside this interval. Empty input sets hi=-1 and returns -1; no rotation is also valid.
Distinctness is essential to identifying the sorted half from endpoint comparisons.

## Why Krama needs it

This develops DSA-24 in its independent track. Use the prerequisite named above;
the other two tracks are not prerequisites. The [day hub](../LESSON.md) preserves the daily budgets.

## The source behind it

[LeetCode 33](https://leetcode.com/problems/search-in-rotated-sorted-array/) specifies rotated distinct values and a logarithmic search target. The elimination proof above is derived from that input contract.
Source links checked 2026-09-22; see [the source ledger](../../../docs/SOURCES.md).
The examples and small failure models below are original teaching demonstrations.

## The mechanism

### Worked trace

Search [8, 10, 12, 1, 3, 5, 6] for 10:

| lo | hi | mid/value | Sorted half and target test | Next interval |
| --- | --- | --- | --- | --- |
| 0 | 6 | 3 / 1 | Right [1..6] sorted; 10 outside (1,6] | [0,2] |
| 0 | 2 | 1 / 10 | Midpoint equals target | return 1 |

Always test equality first. If nums[lo]<=nums[mid], the left half is sorted. Keep it when
nums[lo]<=target<nums[mid] by setting hi=mid-1; otherwise set lo=mid+1. If the left half
is not sorted, the right half is sorted. Keep it when nums[mid]<target<=nums[hi] by setting
lo=mid+1; otherwise set hi=mid-1. The strict midpoint comparisons exclude a value already
checked; the non-strict outer comparisons preserve a target at an endpoint.

Inside a sorted half, an outside-range target cannot occur. When the target is inside that
range, distinct rotation order puts the other half outside it. This justifies either discard.
Every unsuccessful iteration excludes the midpoint and roughly half the remaining indices,
giving O(log n) time and O(1) auxiliary space. A linear index scan is the O(n) oracle.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
def locate(values, target, rotation_aware):
    lo, hi = 0, len(values) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if values[mid] == target:
            return mid
        if not rotation_aware:
            keep_left = target < values[mid]
        elif values[lo] <= values[mid]:
            keep_left = values[lo] <= target < values[mid]
        else:
            keep_left = not (values[mid] < target <= values[hi])
        if keep_left:
            hi = mid - 1
        else:
            lo = mid + 1
    return -1

values = [8, 10, 12, 1, 3, 5, 6]
print('ordinary search:', locate(values, 10, False), 'rotation-aware:', locate(values, 10, True))
assert locate(values, 10, False) == -1
for size in range(8):
    base = list(range(0, size * 2, 2))
    for pivot in range(max(1, size)):
        rotated = base[pivot:] + base[:pivot]
        for target in range(-1, size * 2 + 1):
            expected = rotated.index(target) if target in rotated else -1
            assert locate(rotated, target, True) == expected
print('all tiny rotations checked')
```

**Line by line:** The ordinary branch mistakes the midpoint for a global ordering boundary. The corrected branch determines a sorted half. Exhaustive tiny rotations compare every result with linear search, including absence and empty input.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
ordinary search: -1 rotation-aware: 1
all tiny rotations checked
```

The failing behavior is deliberate; subsequent assertions check the repair on these examples.
An executed Python model does not establish database behavior or production performance.

## In production

Do not sort the input to repair it: sorting loses original indices and costs O(n log n).
Optional changed contract: duplicates can make both endpoints and mid equal while hiding a
seam, as in [1,0,1,1,1]. Resolving that ambiguity may require linear work. Today's logarithmic
proof covers distinct values only. Compare endpoint targets, absent targets, singletons,
unrotated input, and seams on either side of mid.

## Check yourself

### Readiness before practice

1. Why is at least one half sorted?
2. Why must midpoint equality be checked before selecting a half?
3. Which interval convention changed from Day 22, and what is the loop condition now?
4. Why does [1,0,1,1,1] defeat the distinct-value inference?

Use [README.md](README.md) for the assignment, verification, and personal evidence route.
Reading the lesson does not complete study.
