---
day: 30
part: "1.1"
title: "Merge overlapping intervals"
ids: [DSA-30]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Merge overlapping intervals

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

After sorting closed intervals by start, only the last merged interval can overlap the next one.

## The story

A calendar import includes a long block and a shorter block inside it. Replacing the long block’s end with the shorter end silently drops booked time.

## The idea in plain language

Recall [stable sorting](../../day-029-stable-record-sorting/dsa_stable-record-sorting/CONCEPTS.md). A closed interval [a,b] includes both endpoints.
Merging computes the union of covered points, represented as sorted nonoverlapping intervals.
Sorting by start turns arbitrary overlap comparisons into a scan. Keep one active interval
whose end is the farthest end reached by its connected group. Earlier emitted groups are final.

## Why Krama needs it

This develops DSA-30. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Official LeetCode companion](https://leetcode.com/problems/merge-intervals/) defines the online contract; [LEETCODE.md](LEETCODE.md) compares it with local practice.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

Sort [(7,9),(1,8),(2,3),(12,14)] into [(1,8),(2,3),(7,9),(12,14)].

| Next | Active before | Action | Active after |
| --- | --- | --- | --- |
| [2,3] | [1,8] | overlaps; max(8,3) | [1,8] |
| [7,9] | [1,8] | overlaps; extend end | [1,9] |
| [12,14] | [1,9] | gap; emit [1,9] | [12,14] |

Emit the active interval once the scan ends. The invariant is exact coverage of all processed
intervals, with disjoint finalized output before the active group. If next.start>active.end,
every future start is also beyond the active end, so finalization is safe. Otherwise the union
is [active.start,max(active.end,next.end)]. Closed endpoints mean equality overlaps: [1,2] and
[2,4] become [1,4]. A point interval [2,2] is valid under this model.

Sorting dominates O(n log n) time; the scan is O(n). Output may contain n intervals. Python
sorting and a copied input can each use O(n) auxiliary storage; do not call the entire routine
constant-space just because the active state has two numbers. Empty input returns empty output.
The online task shares the closed-endpoint union rule; the local adapter requires sorted output.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
active = [1, 8]
nested = [2, 3]
wrong = [active[0], nested[1]]
fixed = [active[0], max(active[1], nested[1])]
print('overwritten end:', wrong)
print('preserved coverage:', fixed)
assert not (wrong[0] <= 7 <= wrong[1])
assert fixed[0] <= 7 <= fixed[1]
assert 2 <= 2  # Touching closed endpoints overlap.
```

**Line by line:** The nested interval cannot shrink existing coverage. The point 7 is a witness lost by assignment and retained by max. The equality assertion records the endpoint policy independently of the nesting bug.

Observed author output on Python 3.12.10, 2026-09-23:

```text
overwritten end: [1, 3]
preserved coverage: [1, 8]
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Define time zone, precision, and endpoint policy before merging calendar data. Returning
references to input lists can leak later mutations; copy records when ownership requires it.
For an already ordered stream, scan directly without sorting, but validate or document that
ordering promise. Optional depth: disjoint half-open ranges need a separately defined rule
for whether merely adjacent ranges should be coalesced.

## Check yourself

### Readiness before practice

1. Why is comparing only with the active group enough?
2. Which input catches an end that shrinks?
3. Why does [2,2] differ from an empty half-open interval?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.
