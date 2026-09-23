---
day: 20
part: "1.1"
title: "Shrink every qualifying positive window"
ids: [DSA-20]
level: working
prerequisites: ["Day 18 rolling totals; positive integers"]
failure: true
---

# Shrink every qualifying positive window

Core reading: explanation, worked trace, and readiness. The production section offers optional
depth for another sitting; keep the existing track budget and record partial work honestly.

## One-line answer

With positive values, extend until the sum qualifies, then repeatedly record and shrink while it still qualifies.

## The story

A savings log needs the fewest consecutive deposits reaching a target. Once a range reaches
the target, its earliest deposit may be unnecessary; removing just one can miss an even shorter range.

## The idea in plain language

Recognize a shortest nonempty contiguous range with sum >= a positive target. Every input
value is strictly positive, so extending increases the total and removing the left item decreases
it. This monotonicity lets both boundaries move only forward. Keep left, total, and the shortest
qualifying length found so far, with an explicit no-answer sentinel.

Do not confuse this threshold question with [Day 13 exact-sum counting](../../day-013-count-target-subarrays/dsa_count-target-subarrays/CONCEPTS.md),
which supports negatives and must preserve prefix multiplicity. Sliding windows are justified
by the specific condition, not by seeing the word subarray.

## Why Krama needs it

This develops DSA-20 for the [Week 3 review](../../day-021-week-3-review/LESSON.md).
The tracks remain independent; use only this subject's prerequisites.

## The source behind it

[Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/),
LeetCode 209, uses positive integers and a positive target, returning zero if none qualifies.
The local JSON adapter has the same objective. The online O(n log n) follow-up is optional. Checked 2026-09-22; details are in the [source ledger](../../../docs/SOURCES.md).
The trace and counterexample below are original teaching examples.

## The mechanism

### Worked trace

Use [2, 1, 4, 2] with target=6.

| Right | Total after extension | Qualifying lengths recorded before each removal | State after shrinking |
| --- | --- | --- | --- |
| 0 | 2 | none | left=0, total=2 |
| 1 | 3 | none | left=0, total=3 |
| 2 | 7 | 3 | left=1, total=5 |
| 3 | 7 | 3, then 2 | left=3, total=2 |

While total >= target, record right-left+1 before subtracting nums[left] and advancing left.
Stopping after one removal misses the final length 2. After the while loop, the retained
window is below target. For a fixed right, shrinking visits every still-available valid start
until further shrinking cannot qualify, because every removal reduces the sum.

A start discarded at an earlier right already produced a qualifying window. Extending that
same start later only makes it longer, so it cannot improve the shortest answer. This proves
that permanently advancing left loses no better candidate. Both boundaries advance at most n
times: O(n) time, O(1) auxiliary space with indexable input. Enumerating starts and incrementally
extending each is an O(n²) baseline. Empty local input has no qualifying nonempty subarray and
therefore yields zero; the online constraints require nonempty input.

Optional follow-up: positive prefix sums are strictly increasing, so each start can binary
search its earliest qualifying end, giving O(n log n) time and O(n) prefix storage. The linear
window is sufficient for the core session.

## When it breaks

Run this separate teaching demonstration before implementing your own exercise.

```python
def positive_rule(values, target):
    left = total = 0
    best = len(values) + 1
    for right, value in enumerate(values):
        total += value
        while total >= target:
            best = min(best, right - left + 1)
            total -= values[left]
            left += 1
    return 0 if best > len(values) else best

values, target = [1, -1, 5], 5  # deliberately outside the positive contract
wrong = positive_rule(values, target)
oracle = min((j - i for i in range(len(values))
              for j in range(i + 1, len(values) + 1)
              if sum(values[i:j]) >= target), default=0)
print("positive-only rule:", wrong, "oracle with negatives:", oracle)
try:
    assert wrong == oracle, "negative values invalidate the stopping rule"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert positive_rule([2, 1, 4, 2], 6) == 2
```

**Line by line:** The demonstration deliberately applies a positive-input algorithm outside its contract.
Removing 1 leaves total 4, so shrinking stops before removing -1, which would raise it to 5.
The oracle finds the single value 5. The final assertion checks the earlier valid-input trace.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
positive-only rule: 3 oracle with negatives: 1
AssertionError: negative values invalidate the stopping rule
```

**Line by line:** These are the actual printed observations, including the deliberately caught
assertion or exception. A caught failure documents the wrong assumption; later assertions check
the repair on the stated example, not on every possible input.

## In production

Do not silently accept negative adjustments under this proof; a different algorithm is
needed (the later shortest-subarray-with-negatives lesson covers it). Nonnegative zeros can be
supported for a positive target with the same non-strict monotonic reasoning, but today's
contract is strictly positive. Test exact equality, an oversized single value, no answer,
an answer at the end, and multiple successful removals in one extension.

## Check yourself

### Readiness before practice

1. Why record length before removing the left item?
2. Why must shrinking be a while loop rather than one if?
3. What precise inference fails for [1, -1, 5] and target=5?
4. Why can a discarded start never improve the answer at a later endpoint?

Use [README.md](README.md) for the assignment and evidence route. Reading does not complete study.
