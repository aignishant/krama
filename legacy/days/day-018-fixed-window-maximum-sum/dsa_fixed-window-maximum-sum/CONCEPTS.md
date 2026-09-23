---
day: 18
part: "1.1"
title: "Reuse the overlap of fixed windows"
ids: [DSA-18]
level: working
prerequisites: ["Day 12 range sums; adjacent array positions"]
failure: true
---

# Reuse the overlap of fixed windows

Core reading: explanation, worked trace, and readiness. The production section offers optional
depth for another sitting; keep the existing track budget and record partial work honestly.

## One-line answer

Build one k-item sum, then slide by subtracting the departing item and adding the arriving item.

## The story

A dashboard needs the strongest three-day sales total. Readding all three days every
morning repeats two days of work that yesterday's total already contains.

## The idea in plain language

A window is a contiguous interval. Fixed width means every candidate has exactly k items,
not at most k and not an arbitrary subsequence. Adjacent candidates overlap in k-1 positions.
Unlike [Day 12 prefix sums](../../day-012-range-sums/dsa_range-sums/CONCEPTS.md), this query
visits all equal-width ranges in order, so it can retain one running sum instead of a prefix
array. Negative values are valid: the overlap identity does not rely on monotonicity.

Keep the current sum and the best sum, initialized from the first real window. Do not use
zero as an imaginary candidate when every valid sum might be negative.

## Why Krama needs it

This develops DSA-18 for the [Week 3 review](../../day-021-week-3-review/LESSON.md).
The tracks remain independent; use only this subject's prerequisites.

## The source behind it

[Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/),
LeetCode 643, returns an average. Local practice returns a sum. Since k is fixed and positive,
the maximizing window is identical; divide the best sum by k only for the online result. Checked 2026-09-22; details are in the [source ledger](../../../docs/SOURCES.md).
The trace and counterexample below are original teaching examples.

## The mechanism

### Worked trace

Use [4, -2, 5, -1] and k=2.

| Included indices | Previous sum | Remove | Add | New sum | Best |
| --- | --- | --- | --- | --- | --- |
| 0..1 | none | none | first two | 2 | 2 |
| 1..2 | 2 | 4 | 5 | 3 | 3 |
| 2..3 | 3 | -2 | -1 | 4 | 4 |

At incoming index r, remove index r-k. If the old total is the sum of indices r-k through
r-1, subtracting its first term and adding nums[r] gives exactly r-k+1 through r. This is the
maintenance proof. Initialize with indices 0 through k-1, then evaluate every remaining right
endpoint through n-1. There are n-k+1 windows, including the final one.

Initial summation costs O(k); n-k constant-work updates give O(n) total time. An index-based
initial loop and direct accesses need O(1) auxiliary space. sum(nums[:k]) creates an O(k)
temporary slice; summing every slice again costs O(nk). A one-pass external stream needs an
O(k) buffer to remember departing values, unlike an already supplied indexable array.
The online answer is best/k; a variable-width average cannot use this equivalence.

## When it breaks

Run this separate teaching demonstration before implementing your own exercise.

```python
values, k = [-6, -2, -5], 2
sums = [sum(values[i:i + k]) for i in range(len(values) - k + 1)]
wrong = max([0] + sums)
correct = max(sums)
print("window sums:", sums, "zero seed:", wrong, "real seed:", correct)
try:
    assert wrong == correct, "zero is not a valid length-k window"
except AssertionError as error:
    print(f"AssertionError: {error}")
running = values[0] + values[1]
running += values[2] - values[0]
assert running == sums[1]
print("online average:", correct / k)
```

**Line by line:** The tiny slice-based oracle lists both real candidates. Adding zero deliberately invents
an invalid candidate. The incremental update then checks the overlap identity independently.
Division converts the winning sum to the online contract without changing the chosen window.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
window sums: [-8, -7] zero seed: 0 real seed: -7
AssertionError: zero is not a valid length-k window
online average: -3.5
```

**Line by line:** These are the actual printed observations, including the deliberately caught
assertion or exception. A caught failure documents the wrong assumption; later assertions check
the repair on the stated example, not on every possible input.

## In production

For floating-point streams, repeated subtraction can accumulate rounding error; choose a
numeric policy and occasionally recompute if needed. The integer teaching contract avoids that
issue. A fixed window controls count, not elapsed time when samples arrive irregularly.
Test k=1, k=n, all-negative input, ties, and a winner at the final possible start.

## Check yourself

### Readiness before practice

1. Which index leaves when r arrives, and why?
2. Why must best start with a real window?
3. What extra memory appears for a stream without random access?
4. Why can the online average be computed after finding the maximum sum?

Use [README.md](README.md) for the assignment and evidence route. Reading does not complete study.
