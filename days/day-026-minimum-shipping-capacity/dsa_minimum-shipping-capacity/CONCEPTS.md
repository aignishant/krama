---
day: 26
part: "1.1"
title: "Minimum shipping capacity"
ids: [DSA-26]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Minimum shipping capacity

Core reading: intuition, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting. Record partial progress if needed.

## One-line answer

Search capacities with a monotone feasibility test, and pack each day greedily in the required order.

## The story

A delivery van must carry parcels in queue order. Increasing its capacity cannot force an extra trip, but dividing total weight by the deadline can hide an awkward parcel boundary.

## The idea in plain language

Use [answer-space search](../../day-025-integer-square-root/dsa_integer-square-root/CONCEPTS.md).
Capacity is the candidate answer; feasibility asks whether all positive weights fit within D
days. "Within" allows unused days. The parcels cannot be reordered or split. A greedy feasibility
check fills today's load until the next parcel would exceed capacity, then starts another day.
The check and the search are separate claims: first prove the check counts the fewest possible
days for a capacity, then prove feasible capacities form a suffix.

## Why Krama needs it

This develops DSA-26 independently of the other two tracks. The [day hub](../LESSON.md)
links the separate 60/30/15-minute routes; completing the reading is not passing the assignment.

## The source behind it

[Capacity To Ship Packages Within D Days, LeetCode 1011](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) confirms order, indivisibility, and the deadline contract.
Checked 2026-09-23; details are in the [source ledger](../../../docs/SOURCES.md).
The traces, examples, and failure demonstrations here are original teaching material.

## The mechanism

### Worked trace

For weights [4,2,5,3] and D=3, the minimum candidate is max(weights)=5: no parcel can be
split. The maximum is sum(weights)=14: one day suffices. Testing each integer capacity would
take O(n*(S-M+1)) work for S=sum(weights), M=max(weights).

| Candidate capacity | Greedy daily groups | Days | Feasible? |
| --- | --- | --- | --- |
| 9 | [4,2], [5,3] | 2 | yes |
| 7 | [4,2], [5], [3] | 3 | yes |
| 6 | [4,2], [5], [3] | 3 | yes |
| 5 | [4], [2], [5], [3] | 4 | no |

For the search, keep the answer in inclusive [lo,hi], starting [5,14]. If mid works, retain
it with hi=mid; if it fails, use lo=mid+1. The table gives the tested mids 9,7,6,5 and ends
at lo=hi=6. The upper bound always remains a feasible candidate.

Why greedy works: on day one no valid schedule can ship a longer prefix than the greedy fill.
If greedy has shipped at least as far after t days, it can reach at least as far on day t+1
as any alternative: any suffix of that alternative day's positive weights still fits. Induction
therefore shows greedy never needs more days than a valid competing schedule.

Why search works: any grouping feasible at C remains feasible at a larger capacity. A failure
eliminates C and all smaller candidates; success keeps C and eliminates larger answers. Each
iteration shortens the range. Total time is O(n log(S-M+2)), O(1) auxiliary space when scanning
the input directly. The checker must reject a parcel heavier than C if used outside these bounds.
At D=1 the answer is S; at D>=n it is M. Sorting the weights changes the problem.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
weights = [4, 4, 4]
days = 2
average_bound = (sum(weights) + days - 1) // days
groups = [[4], [4], [4]]  # At capacity 6, no adjacent pair fits.
print("average bound:", average_bound, "days actually needed:", len(groups))
assert len(groups) > days
fixed_groups = [[4, 4], [4]]
assert all(sum(group) <= 8 for group in fixed_groups)
assert len(fixed_groups) <= days
print("capacity 8 has a valid ordered schedule")
```

**Line by line:** Ceiling division gives a lower bound of 6 but says nothing about indivisible parcels. The explicit groups show why 6 fails. The repaired grouping preserves order and verifies both the capacity and day limit; it is a witness, not an implementation of solve.

Observed author output on Python 3.12.10, 2026-09-23:

```text
average bound: 6 days actually needed: 3
capacity 8 has a valid ordered schedule
```

The deliberate failure and repaired assertions are teaching evidence, not learner progress.
Python state models do not demonstrate PostgreSQL isolation or production performance.

## In production

Separate model assumptions from operational scheduling. Real vehicles can have volume limits,
delivery windows, or reorderable jobs; those may require a different feasibility algorithm.
If feasibility is expensive, early-stop once days exceed D. Do not cache a verdict across changed
weights. Interview follow-up: identify exactly which greedy proof step would fail if arbitrary
reordering or negative weights were introduced.

## Check yourself

### Readiness before practice

1. Why can a failed capacity eliminate all smaller capacities?
2. Why is ceil(total/D) only a lower bound?
3. Trace a case where a load equals capacity exactly; when does the next day start?
4. What happens when D exceeds the number of parcels?

Run the teaching block only if you need to check your prediction. Then return to
[README.md](README.md) for the assignment, verification, and personal evidence route.
