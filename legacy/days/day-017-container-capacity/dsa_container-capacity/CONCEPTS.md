---
day: 17
part: "1.1"
title: "Discard the limiting wall"
ids: [DSA-17]
level: working
prerequisites: ["Day 15 elimination proof; nonnegative heights"]
failure: true
---

# Discard the limiting wall

Core reading: explanation, worked trace, and readiness. The production section offers optional
depth for another sitting; keep the existing track budget and record partial work honestly.

## One-line answer

Evaluate the widest remaining pair, then discard a shorter wall because keeping it cannot produce a larger area.

## The story

Two fence posts can hold a sheet across a gap, but the shorter post limits its height.
Choosing the two tallest posts sounds promising until you notice that they stand side by side.

## The idea in plain language

Recognize a pair objective with two competing factors: distance and a bottleneck height.
For indices i < j, area is min(h[i], h[j]) times (j-i). Only those two walls determine the
container; interior heights do not change this objective. This is different from summing
water trapped across every position. Heights are nonnegative and positions have unit spacing.

[Day 15](../../day-015-sorted-pair-existence/dsa_sorted-pair-existence/CONCEPTS.md) introduced
elimination by proof. Here the array need not be sorted. Sorting would change the distances
and therefore the problem. Keep left, right, and the best area already evaluated.

## Why Krama needs it

This develops DSA-17 for the [Week 3 review](../../day-021-week-3-review/LESSON.md).
The tracks remain independent; use only this subject's prerequisites.

## The source behind it

[Container With Most Water](https://leetcode.com/problems/container-with-most-water/),
LeetCode 11, supplies the companion contract: at least two nonnegative heights. The local
contract additionally returns zero for fewer than two heights. Checked 2026-09-22; details are in the [source ledger](../../../docs/SOURCES.md).
The trace and counterexample below are original teaching examples.

## The mechanism

### Worked trace

Use [2, 7, 3, 6]. Start with left=0 and right=3.

| Pair | Width | Limiting height | Area | Decision |
| --- | --- | --- | --- | --- |
| (0,3) | 3 | 2 | 6 | Discard index 0 |
| (1,3) | 2 | 6 | 12 | Discard index 3 |
| (1,2) | 1 | 3 | 3 | Discard index 2; stop |

Why discard left when h[left] <= h[right]? For any interior k, the pair (left,k) has
height at most h[left] and a smaller width. Its area cannot exceed the area just recorded.
Thus every pair lost by removing left is already dominated by a checked answer. The argument
is symmetric for removing right. On equal heights, either one can be removed after evaluation.
Nonnegative heights make the width comparison valid even when the limiting height is zero.

Invariant: the best checked value together with pairs inside the remaining interval still
contains a global optimum. The invariant starts with every pair available and survives each
discard. When fewer than two walls remain, the recorded maximum is the answer. Each move
reduces interval width, giving O(n) time and O(1) auxiliary space. Enumerating every pair is
an O(n²) baseline suitable for a tiny oracle. No input mutation or slice is needed.

## When it breaks

Run this separate teaching demonstration before implementing your own exercise.

```python
heights = [1, 3, 3]
left, right = 0, len(heights) - 1
wrong = 0
while left < right:
    wrong = max(wrong, min(heights[left], heights[right]) * (right - left))
    if heights[left] < heights[right]:
        right -= 1  # deliberately discard the taller wall
    else:
        left += 1
oracle = max(min(heights[i], heights[j]) * (j - i)
             for i in range(len(heights)) for j in range(i + 1, len(heights)))
print("wrong move:", wrong, "all pairs:", oracle)
try:
    assert wrong == oracle, "discarded the wall needed by the best pair"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert min(heights[1], heights[2]) * (2 - 1) == oracle
```

**Line by line:** The loop intentionally moves the taller endpoint and loses pair (1,2). The nested
oracle examines each distinct index pair independently. The last assertion confirms the
lost pair's value; the learner still implements the correct linear scan.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
wrong move: 2 all pairs: 3
AssertionError: discarded the wall needed by the best pair
```

**Line by line:** These are the actual printed observations, including the deliberately caught
assertion or exception. A caught failure documents the wrong assumption; later assertions check
the repair on the stated example, not on every possible input.

## In production

For irregular positions, use their actual sorted coordinates for width; never sort heights
independently. Establish nonnegative heights and valid units before applying the proof. Large
integer multiplication is not unit cost in Python, although interview analysis normally uses
that model. Test zeros, two walls, equal heights, increasing heights, and a narrow tall pair.

## Check yourself

### Readiness before practice

1. Why does moving the taller wall have no elimination proof?
2. Trace [4, 4, 4] and justify either move at equality.
3. Why does sorting heights invalidate the objective?
4. How does the local empty-input rule differ from the companion?

Use [README.md](README.md) for the assignment and evidence route. Reading does not complete study.
