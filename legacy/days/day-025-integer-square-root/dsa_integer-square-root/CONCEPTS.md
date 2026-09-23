---
day: 25
part: "1.1"
title: "Integer square root"
ids: [DSA-25]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Integer square root

Core reading: intuition, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting. Record partial progress if needed.

## One-line answer

An integer square root is the last integer whose square does not exceed the input.

## The story

You have 30 floor tiles and want the largest complete square. Five tiles per side use 25; six need 36. You need a boundary, not a decimal approximation.

## The idea in plain language

Start with [lower-bound search](../../day-022-lower-bound/dsa_lower-bound/CONCEPTS.md).
A predicate is a yes/no test on a candidate. Here the candidates are nonnegative integers k,
and the test is k*k <= n. As k increases, the answers are true and then false. This is called
monotonicity: after the test becomes false, it cannot become true again.

Recognize this pattern when the answer is an extremal number and testing a candidate is easier
than constructing the answer. We seek the last true candidate, whereas lower bound seeks a first
boundary. A baseline tries successive k values, taking O(sqrt(n)+1) tests. Binary search discards
whole ranges because every larger square is at least as large.

## Why Krama needs it

This develops DSA-25 independently of the other two tracks. The [day hub](../LESSON.md)
links the separate 60/30/15-minute routes; completing the reading is not passing the assignment.

## The source behind it

[Sqrt(x), LeetCode 69](https://leetcode.com/problems/sqrtx/) supplies the companion contract; the invariant proof above is derived here.
Checked 2026-09-23; details are in the [source ledger](../../../docs/SOURCES.md).
The traces, examples, and failure demonstrations here are original teaching material.

## The mechanism

### Worked trace

Use two *sentinel bounds*: lo is known feasible and hi is known infeasible. Initially lo=0
and hi=n+1; even n=0 satisfies 0*0 <= n < (n+1)*(n+1). While hi-lo > 1, try the midpoint.
If its square fits, replace lo; otherwise replace hi. Neither bound is an arbitrary guess.

For n=30:

| lo | hi | midpoint | Test | New information |
| --- | --- | --- | --- | --- |
| 0 | 31 | 15 | 225 > 30 | hi=15 |
| 0 | 15 | 7 | 49 > 30 | hi=7 |
| 0 | 7 | 3 | 9 <= 30 | lo=3 |
| 3 | 7 | 5 | 25 <= 30 | lo=5 |
| 5 | 7 | 6 | 36 > 30 | hi=6 |

The invariant lo² <= n < hi² survives each update. The interval strictly shrinks; when the
bounds are adjacent, no integer between them remains, so lo is the floor root. Test n=0, n=1,
a perfect square, and its two neighbors. Equality belongs to the feasible side.

Cost is O(log(n+1)) comparisons and O(1) integer variables in the usual unit-cost model.
For arbitrary Python integers, multiplication and storage depend on bit length. In a fixed-width
language avoid overflow by comparing mid <= n//mid when mid>0. Do not introduce division by zero.
The local route forbids square-root functions; the online companion also prohibits fractional
exponent shortcuts. Use exact integer arithmetic in either route.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
n = 16
wrong = max(k for k in range(n + 1) if k * k < n)
right = max(k for k in range(n + 1) if k * k <= n)
print("strict comparison:", wrong, "inclusive comparison:", right)
assert wrong != 4
assert right * right <= n < (right + 1) * (right + 1)
print("boundary certificate passed")
```

**Line by line:** The two enumerations are small-input oracles, not the requested optimized implementation. Changing only < to <= isolates the equality bug. The final chained comparison certifies the floor-root contract on both sides.

Observed author output on Python 3.12.10, 2026-09-23:

```text
strict comparison: 3 inclusive comparison: 4
boundary certificate passed
```

The deliberate failure and repaired assertions are teaching evidence, not learner progress.
Python state models do not demonstrate PostgreSQL isolation or production performance.

## In production

A reviewer should ask for the two inequalities certifying the result, not accept an approximate
float followed by truncation. Near large perfect squares, precision can change which side of the
boundary a value appears to occupy. A standard exact integer-root function can be appropriate in
application code when the exercise restriction is absent. Optional depth: compare integer
arithmetic costs or derive an iterative numerical method with an exact final correction.

## Check yourself

### Readiness before practice

1. Why is n+1 a valid infeasible sentinel even when n=0?
2. Trace n=15 and n=16; which branch handles equality?
3. What prevents a two-candidate interval from looping forever?
4. Why does finding any feasible k fail to prove it is the answer?

Run the teaching block only if you need to check your prediction. Then return to
[README.md](README.md) for the assignment, verification, and personal evidence route.
