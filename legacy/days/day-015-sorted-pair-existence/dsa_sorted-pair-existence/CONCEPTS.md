---
day: 15
part: "1.1"
title: "Use sorted order to discard impossible pairs"
ids: [DSA-15]
level: working
prerequisites: ["Sorted arrays", "Distinct indices"]
failure: true
---

# Use sorted order to discard impossible pairs

Core: explanation, worked trace, and readiness. Production extensions are optional depth;
continue another sitting if needed within the existing track budget.

## One-line answer

Compare the two ends of a sorted interval and discard only the endpoint that cannot belong to any remaining answer.

## The story

You have prices listed from cheapest to most expensive and want two items matching a budget. Pairing the cheapest remaining item with the most expensive gives a useful bound on every other pair involving that cheapest item.

## The idea in plain language

Two pointers are indices delimiting candidates. Sorting makes values monotone: moving right
cannot decrease a value. If the endpoint sum is too small, even the largest partner cannot
make the left value work. If it is too large, even the smallest partner cannot make the right
value work. This is a proof of elimination, not a guess about moving toward a target.
[Day 10](../../day-010-pair-sum-indices/dsa_pair-sum-indices/CONCEPTS.md) used a dictionary on
unsorted input; sorted input permits constant auxiliary state. Equal values are allowed, but
two distinct positions are required.

## Why Krama needs it

[Day 16](../../day-016-unique-triples/dsa_unique-triples/CONCEPTS.md) fixes one value and searches the remaining sorted suffix for a pair.

## The source behind it

[Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) (LeetCode 167) returns one-based indices, promises one solution, and requires constant extra space. Local practice returns a boolean and permits no answer. Checked 2026-09-22; see the dated [source ledger](../../../docs/SOURCES.md).

## The mechanism

### Worked trace

For `[-3, 1, 4, 7, 10]`, target 8:

| Left, right | Sum | Justified move |
| --- | --- | --- |
| 0, 4 | 7 | Drop -3: every available partner is at most 10 |
| 1, 4 | 11 | Drop 10: every available partner is at least 1 |
| 1, 3 | 8 | Found distinct positions |

Invariant: if an answer remains undiscovered, one lies wholly inside the active interval.
Each elimination rules out all pairs involving the discarded endpoint and preserves that
invariant. A match proves existence. When left meets right, no distinct pair remains, proving
absence. Each move shortens the interval, so there are at most n-1 comparisons, O(n) time and
O(1) auxiliary space. An O(n²) pair enumeration is a useful small-input oracle.
For the online route, convert a discovered pair to one-based positions only at return time.

## When it breaks

```python
values = [5]
left = right = 0
wrong = left <= right and values[left] + values[right] == 10
correct = left < right and values[left] + values[right] == 10
print("allow same index:", wrong, "distinct indices:", correct)
try:
    assert wrong == correct, "one item was used twice"
except AssertionError as error:
    print(f"AssertionError: {error}")
```

**Line by line:** The one-element list isolates the termination condition. Both sums use the same value, but only the strict bound respects the two-index contract. The assertion exposes the false positive.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
allow same index: True distinct indices: False
AssertionError: one item was used twice
```

Unsorted `[4, 1, 5]`, target 6, defeats the sorted elimination: discarding 5 from the initial
sum 9 loses the pair 1+5. Verify the precondition rather than applying a memorized move.

## In production

Sorting an unsorted copy adds O(n log n) time and O(n) copied storage; original indices need explicit preservation. Python sorting may need O(n) workspace even when mutating a list in place. A reviewer should ask whether data arrives sorted, whether mutation is allowed, and whether the result is values, existence, or original positions.

## Check yourself

### Readiness before practice

1. Prove why a sum below target rules out the left endpoint.
2. Why does `[5, 5]` differ from `[5]` for target 10?
3. How does the online return type differ?
4. Why does sorting change the cost claim on unsorted input?

Run the teaching block in a scratch interpreter, then explain the distinguishing failure aloud.
Use [README.md](README.md) to enter the assignment and record your own evidence.
