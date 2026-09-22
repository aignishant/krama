---
day: 22
part: "1.1"
title: "Find the first true boundary"
ids: [DSA-22]
level: working
prerequisites: ["Sorted arrays; integer indices and half-open ranges"]
failure: true
---

# Find the first true boundary

Core reading: explanation, worked trace, and readiness within the existing track cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Lower bound finds the first index whose value is at least the target, keeping known-false and known-true regions outside the search interval.

## The story

A sorted price list contains repeated prices. Finding any matching price is insufficient when a new entry must be inserted before all equal prices.

## The idea in plain language

A nondecreasing array turns `nums[i] >= target` into a false-then-true predicate.
Recognize a first qualifying position, including an insertion point when the target is absent.
Use the half-open element interval [lo, hi): lo starts at 0, hi at n. Indices before lo are
known too small; existing indices at or after hi are known large enough. The answer is a
boundary in [lo, hi], including n. That boundary is not necessarily a readable array index.
Duplicates are permitted locally. Do not sort inside the function: sorted input is the premise.

## Why Krama needs it

This develops DSA-22 in its independent track. Use the prerequisite named above;
the other two tracks are not prerequisites. The [day hub](../LESSON.md) preserves the daily budgets.

## The source behind it

[Python bisect partition semantics](https://docs.python.org/3.12/library/bisect.html) and [LeetCode 35](https://leetcode.com/problems/search-insert-position/) support the boundary and companion contracts.
Source links checked 2026-09-22; see [the source ledger](../../../docs/SOURCES.md).
The examples and small failure models below are original teaching demonstrations.

## The mechanism

### Worked trace

For values [2, 4, 4, 9, 12] and target 4:

| lo | hi | mid | Observation | Update |
| --- | --- | --- | --- | --- |
| 0 | 5 | 2 | 4 qualifies; an earlier value may qualify | hi=2 |
| 0 | 2 | 1 | 4 qualifies | hi=1 |
| 0 | 1 | 0 | 2 is too small | lo=1 |

At lo=hi=1 the partition is complete. If mid is too small, sorted order proves that every
index through mid is too small, so lo=mid+1. Otherwise mid may be the answer, so hi=mid.
The uncertain interval shrinks on both branches. Equality must follow the qualifying branch;
returning the first equality encountered gives an arbitrary duplicate.

For target 13 the answer is 5, one past the end. Empty input yields 0 without reading an
element. A linear first-match scan is an O(n) baseline. Halving an indexable interval takes
O(log n) comparisons (O(1) for empty input), O(1) auxiliary storage, and one integer output.
Do not slice the list at each step or assume linked-list midpoint access is constant time.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
from bisect import bisect_left

def boundary(values, target, wrong_equality=False):
    lo, hi = 0, len(values)
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] < target or (wrong_equality and values[mid] == target):
            lo = mid + 1
        else:
            hi = mid
    return lo

values = [2, 4, 4, 9, 12]
print('discarding equals:', boundary(values, 4, True), 'lower bound:', boundary(values, 4))
assert boundary(values, 4, True) == 3
for data in ([], [4], [4, 4], values):
    for target in (0, 4, 13):
        assert boundary(data, target) == bisect_left(data, target)
print('boundary checks passed')
```

**Line by line:** The optional wrong branch discards equality and actually finds an upper bound. The standard-library oracle checks empty, duplicate, and outside-range cases; it is teaching verification, not a replacement for your own exercise.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
discarding equals: 3 lower bound: 1
boundary checks passed
```

The failing behavior is deliberate; subsequent assertions check the repair on these examples.
An executed Python model does not establish database behavior or production performance.

## In production

Distinguish finding a position from inserting: inserting into a Python list can shift O(n)
items even when search is logarithmic. A changed sort key or concurrent mutation can invalidate
the partition. The online companion uses distinct values and a judge method; the local JSON
adapter also admits duplicates and empty input. Both ask for a zero-based insertion boundary.

## Check yourself

### Readiness before practice

1. What is known about indices before lo and at or after hi?
2. Why does equality set hi=mid instead of returning immediately?
3. Why can n be a correct answer but never a valid element access?
4. What makes lo=mid unsafe when hi=lo+1?

Use [README.md](README.md) for the assignment, verification, and personal evidence route.
Reading the lesson does not complete study.
