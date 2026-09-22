---
day: 16
part: "1.1"
title: "Fix one value and enumerate unique pairs"
ids: [DSA-16]
level: working
prerequisites: ["Day 15 pair elimination", "Lexicographic order"]
failure: true
---

# Fix one value and enumerate unique pairs

Core: explanation, worked trace, and readiness. Production extensions are optional depth;
continue another sitting if needed within the existing track budget.

## One-line answer

Sort, fix each distinct first value, and search its suffix while skipping only duplicate value combinations.

## The story

A report lists three adjustments that cancel each other. Several adjustments have the same amount, so the report must distinguish using two real entries from printing the same value combination twice.

## The idea in plain language

A triple uses three distinct indices but is unique by its values. After sorting, represent
each answer as a <= b <= c. Fixing a leaves the pair target -a, handled by
[Day 15](../../day-015-sorted-pair-existence/dsa_sorted-pair-existence/CONCEPTS.md).
The suffix restriction places both other indices after the fixed one, preventing reuse and
permutations. Duplicate skipping removes repeated answers; it must not remove input multiplicity
before searching. Two copies of -1 can legitimately form `[-1, -1, 2]`.

## Why Krama needs it

The [Week 3 review](../../day-021-week-3-review/dsa_week-3-dsa-review/README.md) tests whether you can explain sorted elimination and duplicate handling separately.

## The source behind it

[3Sum](https://leetcode.com/problems/3sum/) (LeetCode 15) requires unique zero-sum triples and accepts arbitrary answer order. The local contract requires internal sorting and lexicographically sorted output; input may be reordered. Checked 2026-09-22; see the dated [source ledger](../../../docs/SOURCES.md).

## The mechanism

### Worked trace

Sort `[-2, 0, 0, 2, 2]`. Fix -2 at index 0, with left=1 and right=4.
The sum is zero, so emit `[-2, 0, 2]`. Move both pointers inward and pass any remaining
copies of the just-used left and right values; no new value combination is lost. The remaining
zero copies would only reproduce the emitted triple. Fixing 0 next leaves `[0, 2, 2]`, whose
smallest possible pair sum is positive; no answer. Skip the next fixed 0 because the earlier
0 already had access to every possible suffix pair for that first value.

For a sum below zero advance left; above zero retreat right. The Day 15 elimination proof
applies to each fixed value. For any valid sorted triple, the first occurrence of its first
value has enough suffix occurrences to find it. At equality, reusing a matched left value
would require the same right value, so skipping duplicates cannot lose a different answer.
These facts establish completeness and uniqueness together.

Sorting is O(n log n); at most n suffix scans each take O(n), giving O(n²) time. With sorted
fixed values and increasing left values, emitted triples are already lexicographic, so no
final result sort is needed. Python sorting can use O(n) workspace; a sorted copy uses O(n)
storage. Report O(m) output for m triples separately. An explicit final sort of answers adds
O(m log m). The O(n³) distinct-index baseline is useful only as a tiny oracle.

## When it breaks

```python
from itertools import combinations
values = [-1, -1, 2]
correct = sorted({tuple(sorted(t)) for t in combinations(values, 3) if sum(t) == 0})
wrong = sorted({tuple(sorted(t)) for t in combinations(set(values), 3) if sum(t) == 0})
print("retain occurrences:", correct, "deduplicate input:", wrong)
try:
    assert wrong == correct, "input deduplication removed a necessary occurrence"
except AssertionError as error:
    print(f"AssertionError: {error}")
```

**Line by line:** combinations enumerates distinct positions as an independent tiny oracle. Sorting each tuple canonicalizes its values; the outer set removes repeated answers. Applying set to the input first destroys multiplicity and loses the only answer.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
retain occurrences: [(-1, -1, 2)] deduplicate input: []
AssertionError: input deduplication removed a necessary occurrence
```

## In production

Output itself can be quadratic, so a caller demanding every triple cannot expect linear memory including results. Streaming can avoid retaining output but changes the interface. For large numeric domains, state the arithmetic model. Keep deduplication tied to the answer contract: an application asking for every index triple needs a different algorithm and potentially cubic output.

## Check yourself

### Readiness before practice

1. Why must the pair search start after the fixed index?
2. Trace `[0, 0, 0, 0]` and explain why exactly one triple remains.
3. Why is removing duplicates from input incorrect?
4. Which costs remain when sorting is called in place?

Run the teaching block in a scratch interpreter, then explain the distinguishing failure aloud.
Use [README.md](README.md) to enter the assignment and record your own evidence.
