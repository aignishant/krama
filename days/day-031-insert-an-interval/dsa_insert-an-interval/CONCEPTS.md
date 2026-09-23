---
day: 31
part: "1.1"
title: "Insert an interval"
ids: [DSA-31]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Insert an interval

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Insert into sorted disjoint intervals by copying a prefix, growing one merged interval, and copying the suffix.

## The story

A new calendar block bridges two existing blocks. An insertion that stops after the first overlap leaves two overlapping entries in the result.

## The idea in plain language

Use [closed-interval merging](../../day-030-merge-overlapping-intervals/dsa_merge-overlapping-intervals/CONCEPTS.md) as the prerequisite. The stronger input
promise—sorted and disjoint—has already done the work that Day 30 needed sorting for.
Split the existing list into intervals entirely before, overlapping, and entirely after the
new interval. The boundary of the overlapping group can move as the new interval grows.

## Why Krama needs it

This develops DSA-31. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Official LeetCode companion](https://leetcode.com/problems/insert-interval/) defines the online contract; [LEETCODE.md](LEETCODE.md) compares it with local practice.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

Insert [3,9] into [[0,1],[2,4],[6,8],[9,11],[15,16]]. Copy [0,1] because its end<3.
Absorb [2,4] to obtain [2,9], then [6,8] without shrinking, then [9,11] because 9<=9.
Now active=[2,11]; the next start 15 is greater than 11. Emit active once and append [15,16].

Maintain three phases. First copy while old.end<new.start. Then absorb while
old.start<=active.end, updating both endpoints by min and max. Finally append the merged
interval and remaining suffix. Strict less-than in the first phase and less-than-or-equal
in the second encode closed endpoints. Comparing against the original end after it has
grown can prematurely stop a connected merge.

The copied prefix cannot overlap the growing interval: input intervals were disjoint, and
the earliest absorbed interval starts after that prefix ends. The suffix cannot overlap it
when its first start exceeds the final active end. Every input interval is visited once:
O(n) time, O(n) returned storage, O(1) scan state excluding output. Sorting again is correct
for a more general input but wastes the promised ordering. Empty input returns just the new
interval; insertion before, after, inside, or across all intervals follows the same phases.
The online task has the same ordering and overlap assumptions with a different signature.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
old = [[1, 3], [5, 7]]
new = [3, 5]
wrong = [old[0], new, old[1]]  # Treating equality as a gap.
fixed = [[1, 7]]
def disjoint_closed(intervals):
    return all(a[1] < b[0] for a, b in zip(intervals, intervals[1:]))
print('wrong output disjoint:', disjoint_closed(wrong))
print('merged bridge:', fixed)
assert not disjoint_closed(wrong)
assert disjoint_closed(fixed)
assert min(x[0] for x in wrong) == fixed[0][0]
assert max(x[1] for x in wrong) == fixed[0][1]
```

**Line by line:** The example bridges two intervals exactly at their endpoints. Adjacent pairs in the wrong output share a point, so the strict disjointness check rejects them. Min and max retain the coverage extrema in the corrected one-group example.

Observed author output on Python 3.12.10, 2026-09-23:

```text
wrong output disjoint: False
merged bridge: [[1, 7]]
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Make sorted/disjoint input an explicit API precondition or validate it in a linear pass.
For many updates, copying an entire list per insertion may dominate; consider an ordered
interval structure once measured workload justifies it. Binary search can find candidate
boundaries quickly but does not remove the O(n) cost of materializing an array result.
A reviewer should distinguish search cost from output construction cost.

## Check yourself

### Readiness before practice

1. Why can the overlap test use the growing end?
2. Which comparisons change for half-open inputs?
3. Why does binary-searching the insertion position not guarantee O(log n) total work?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.
