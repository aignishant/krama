---
day: 12
part: "1.1"
title: "Subtract two boundaries to reuse earlier sums"
ids: [DSA-12]
level: working
prerequisites: ["Running totals", "Inclusive intervals"]
failure: true
---

# Subtract two boundaries to reuse earlier sums

Core: prefix boundaries, inclusive queries, and preprocessing once. Updates and numerical
precision are optional depth; the assigned data is immutable integers.

## One-line answer

Store the sum before each position, then answer inclusive [left, right] with prefix[right+1] minus prefix[left].

## The story

A shop repeatedly totals receipts over different consecutive date ranges. Adding the same
receipts for every question repeats work. A running total at each boundary lets the shop subtract
everything before the requested range from everything through its last day.

## The idea in plain language

A prefix is an initial segment. Define P[t] as the sum of exactly the first t values, including
P[0] = 0 for no values. It is a boundary array with n+1 entries for n inputs. This differs from
an array where entry i means the sum through index i; mixing these definitions causes off-by-one bugs.
Recall [inclusive intervals](../../day-004-reverse-a-segment/dsa_reverse-a-segment/CONCEPTS.md).

Recognize prefix sums when many contiguous-range queries share an unchanged input. Summing
each range separately costs O(nq) in the worst case for q queries. Precomputation pays once
for information reused by every query. Negative values do not interfere: cancellation uses
addition and subtraction, not sorted order or a monotone total.

## Why Krama needs it

[Count target subarrays](../../day-013-count-target-subarrays/dsa_count-target-subarrays/README.md)
will rearrange P[right] - P[left] = target into a lookup of an earlier total. Clear boundary
meaning prevents accidentally counting the wrong interval there.

## The source behind it

[Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/)
(`spec:leetcode-303`, checked 2026-09-22) uses `NumArray(nums)` and repeated
`sumRange(left, right)` calls. The local adapter returns a list for the supplied batch of queries
and permits an empty input only with no queries.

## The mechanism

### Worked trace

For `[3, -2, 6, 1]`:

| Boundary t | Values before boundary | P[t] |
| --- | --- | --- |
| 0 | none | 0 |
| 1 | 3 | 3 |
| 2 | 3, -2 | 1 |
| 3 | 3, -2, 6 | 7 |
| 4 | 3, -2, 6, 1 | 8 |

Build the next boundary by adding the next value to the previous boundary sum. The invariant
starts at the empty prefix and survives each addition, so every entry has the stated meaning.
For inclusive [1, 2], P[3] includes 3, -2, 6 and P[1] includes only 3. Subtraction cancels the
shared prefix, leaving -2 + 6 = 4. For [0, 3], subtract P[0]; for [2, 2], subtract P[2] from P[3].
The initial zero makes both boundaries ordinary cases.

Building takes O(n) time, each query O(1), and all q answers O(n+q) total time. Auxiliary storage
is O(n); the returned local result is O(q) output space. The constructor in the online route
should build once; rebuilding during every `sumRange` forfeits the benefit. A direct indexed
loop can sum a range with O(1) auxiliary storage; Python slicing first creates another list.

## When it breaks

```python
values = [3, -2, 6, 1]
prefix = [0]
for value in values:
    prefix.append(prefix[-1] + value)
left, right = 1, 2
wrong = prefix[right] - prefix[left]
correct = prefix[right + 1] - prefix[left]
print("prefix:", prefix)
print("missing endpoint:", wrong, "inclusive:", correct)
try:
    assert wrong == sum(values[left:right + 1]), "right endpoint was excluded"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert correct == 4
```

**Line by line:** `[0]` represents the empty prefix. Appending adds exactly the new value.
The wrong expression ends before the last requested element. `right + 1` selects the boundary
after it. The slice sum is an independent tiny oracle, not the query implementation.

Author verification on Python 3.12.10, 2026-09-22:

```text
prefix: [0, 3, 1, 7, 8]
missing endpoint: -2 inclusive: 4
AssertionError: right endpoint was excluded
```

## In production

An update at index i invalidates every later boundary. If values change frequently, rebuilding
may be too expensive; [Day 117](../../day-117-mutable-range-sums/dsa_mutable-range-sums/README.md)
introduces a representation supporting updates. Do not silently return stale cached sums.
Python integers avoid fixed-width overflow but arithmetic cost grows with bit length; other
languages need a sufficiently wide accumulator. Floating-point prefix subtraction can lose
precision. A reviewer should ask about update frequency, numeric range, and whether query
validation belongs in the public API rather than relying on interview preconditions.

## Check yourself

### Readiness before practice

1. What exactly does P[2] include, and why are there n+1 entries?
2. Derive the answer for a one-element range without a special branch.
3. Why do negative values work even when prefix totals decrease?
4. Which entries become stale after changing the first value?

Run the block and explain the cancellation aloud. Choose [PRACTICE.md](PRACTICE.md) or
[LEETCODE.md](LEETCODE.md); test first/last endpoints, singletons, negative totals, and repeated queries.

[Navigation](README.md) · [Recall](../../../docs/DSA_RECALL.md#day-012-range-sums)
