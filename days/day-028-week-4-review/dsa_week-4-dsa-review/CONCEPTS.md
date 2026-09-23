---
day: 28
part: "1.1"
title: "Week 4 DSA review"
ids: [DSA-28]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Week 4 DSA review

Cold review: attempt the task in [README.md](README.md) without this lesson first.
Use this explanation afterwards for repair and record any help.

Core reading: intuition, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting. Record partial progress if needed.

## One-line answer

A binary-search review is passed by defending the predicate, bounds, direction, and stopping condition on two cold solves.

## The story

A search passes the sample but freezes when only two positions remain. The remembered template was not enough to explain why every iteration must remove a candidate.

## The idea in plain language

This is repair reading after the cold attempts. Revisit [lower bound](../../day-022-lower-bound/dsa_lower-bound/CONCEPTS.md)
and [shipping capacity](../../day-026-minimum-shipping-capacity/dsa_minimum-shipping-capacity/CONCEPTS.md)
only after trying the assigned problems. The common model is an ordered boundary: a predicate
divides candidates into regions. The meaning of the bounds determines which updates are legal.
Do not memorize one pair of assignments and reuse it without naming that meaning.

## Why Krama needs it

This develops DSA-28 independently of the other two tracks. The [day hub](../LESSON.md)
links the separate 60/30/15-minute routes; completing the reading is not passing the assignment.

## The source behind it

[Search Insert Position, LeetCode 35](https://leetcode.com/problems/search-insert-position/) and [Capacity To Ship Packages Within D Days, LeetCode 1011](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) are the existing review companions.
Checked 2026-09-23; details are in the [source ledger](../../../docs/SOURCES.md).
The traces, examples, and failure demonstrations here are original teaching material.

## The mechanism

### Worked trace

Keep the established 60-minute gate: 5 recall, 20 first re-solve, 20 second re-solve,
10 critique, 5 log. Start from blank code on Day 22 lower bound, then Day 26 shipping capacity.
A harder unresolved problem may replace the second slot. Local Day 28 fixtures cover only the
shipping problem; the first re-solve needs its own tests. Reading a reference counts as help.

After the attempts, compare your invariant with this repair map:

| Mechanism | Boundary being sought | Evidence to defend |
| --- | --- | --- |
| Day 22 lower bound | first value >= target | prefix is smaller; returned index can equal length |
| Day 23 target range | first >= and first > target | absent target and equal-value runs |
| Day 24 rotated search | sorted half containing target | distinctness justifies choosing a half |
| Day 25 square root | last k with k²<=n | result²<=n<(result+1)² |
| Day 26 shipping | first feasible capacity | greedy check correct; feasibility monotone |
| Day 27 median | cut satisfying both cross checks | balanced ranks and sorted cross-boundaries |

Trace the bug before fixing it: inclusive candidates [0,1], midpoint floor=0, and an update
lo=mid leaves [0,1] unchanged. If failure proves mid cannot be the answer, lo=mid+1 removes it.
If lo is a known feasible sentinel in a different algorithm, adjacency should terminate the
loop instead. These are distinct valid contracts; mixing them causes the failure.

For each solve explain initialization, preservation, and termination. Add a boundary test that
would reject your actual wrong update. Lower bound costs O(log(n+1)); shipping costs O(n)
per candidate test times logarithmically many capacities. Score correctness, explanation,
complexity, and tests 0–2 each. The gate requires 6/8 with correctness=2 and at least one
hint-free solve, using both scheduled attempts. If you cannot finish, record a repair session.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
lo, hi = 0, 1
before = (lo, hi)
mid = (lo + hi) // 2
lo = mid
print("stalled interval:", before, "->", (lo, hi))
assert (lo, hi) == before
lo = mid + 1  # Here the failed predicate rules out mid itself.
print("repaired interval:", (lo, hi))
assert lo == hi == 1
```

**Line by line:** The example executes one stalled step instead of hanging in an infinite loop. before records the interval, and the first assertion confirms no progress. The repaired step is justified only for a predicate that rules out mid; the last assertion shows termination on this boundary case.

Observed author output on Python 3.12.10, 2026-09-23:

```text
stalled interval: (0, 1) -> (0, 1)
repaired interval: (1, 1)
```

The deliberate failure and repaired assertions are teaching evidence, not learner progress.
Python state models do not demonstrate PostgreSQL isolation or production performance.

## In production

In code review, require a small certificate or invariant comment instead of a vague statement
that the input is sorted. Changes to duplicate policy, range endpoints, or allowed empty inputs
can invalidate a previously correct search. Optional depth belongs in a later repair sitting:
generate small sorted arrays and compare with a linear oracle. Preserve original cold evidence
even after a repaired implementation passes.

## Check yourself

### Readiness before practice

After attempting: can you explain why each bound moves, prove progress on two candidates,
and name the exact counterexample your new test catches? Which topic still needs another
independent attempt? Do not use these prompts to replace the two assigned re-solves.

Run the teaching block only if you need to check your prediction. Then return to
[README.md](README.md) for the assignment, verification, and personal evidence route.
