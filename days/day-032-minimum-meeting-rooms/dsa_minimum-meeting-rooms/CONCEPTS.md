---
day: 32
part: "1.1"
title: "Minimum meeting rooms"
ids: [DSA-32]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Minimum meeting rooms

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Minimum rooms equals peak overlap, and endpoint event order must match the interval contract.

## The story

One meeting ends at 11 as another starts. Counting both as active at that instant buys an unnecessary room for a calendar that permits immediate reuse.

## The idea in plain language

Recall [interval endpoints](../../day-030-merge-overlapping-intervals/dsa_merge-overlapping-intervals/CONCEPTS.md). Local meetings are positive-length half-open
intervals [start,end): present at start, absent at end. Create a +1 start event and a -1 end
event. A sweep processes time in order and keeps the current active count and its maximum.
This answers how many overlap, not the merged union: a union discards multiplicity.

## Why Krama needs it

This develops DSA-32. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Official LeetCode companion](https://leetcode.com/problems/divide-intervals-into-minimum-number-of-groups/) defines the online contract; [LEETCODE.md](LEETCODE.md) compares it with local practice.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

For [1,4), [2,4), [4,6), visit start 1 -> active 1, start 2 -> active 2,
end 4 -> 1, end 4 -> 0, start 4 -> 1, end 6 -> 0. Peak=2. Process ends before starts
at equal times. With (time,delta) tuples, ascending delta puts -1 before +1.

Peak overlap is a lower bound because simultaneously active meetings require different rooms.
It is achievable by assigning each next meeting a freed room if any, or opening one otherwise.
A min-heap of active end times implements that allocation: discard ends<=next.start for the
local contract, push its end, and track maximum active heap size. The heap needs only the
earliest end to know whether anything has finished; ordering all active meetings is unnecessary.
This greedy allocation never creates a room while one is free, so it uses the lower bound.

Sorting events or meetings costs O(n log n); event storage or a heap uses O(n). Empty local
input has peak 0. Zero-length intervals are excluded locally. The online groups problem uses
CLOSED intervals and permits point intervals: starts must precede ends at ties, or the heap
may free a room only when end<next.start. [1,4] and [4,6] require two online groups but their
half-open versions need one room. Changing the inequality is part of the proof, not cosmetics.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
intervals = [(1, 4), (4, 6)]
events = [(s, 1) for s, e in intervals] + [(e, -1) for s, e in intervals]
def peak(closed):
    active = best = 0
    for time, delta in sorted(events, key=lambda x: (x[0], -x[1] if closed else x[1])):
        active += delta
        best = max(best, active)
    return best
print('wrong local closed policy:', peak(True))
print('correct half-open policy:', peak(False))
assert peak(True) == 2 and peak(False) == 1
```

**Line by line:** Every meeting contributes a start and end event. The sort key toggles only tie ordering. Accumulation is unchanged, isolating the endpoint policy as the cause of the different peaks.

Observed author output on Python 3.12.10, 2026-09-23:

```text
wrong local closed policy: 2
correct half-open policy: 1
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

A real scheduler also needs room identities and possibly cleanup time. Add cleanup time
to an effective end only after defining its units and whether it applies to every meeting.
Do not use float epsilon hacks for endpoint equality; model time precisely. Sorting works
for an offline batch; live cancellation or arbitrary insertion needs additional state.
Optional follow-up: can a count-only sweep reconstruct a room assignment without more data?

## Check yourself

### Readiness before practice

1. Why is peak overlap both a lower bound and achievable?
2. Which event comes first at a local tie?
3. What distinguishes the online closed-interval contract?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.
