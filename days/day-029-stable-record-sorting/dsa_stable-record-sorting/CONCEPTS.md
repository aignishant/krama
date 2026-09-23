---
day: 29
part: "1.1"
title: "Stable record sorting"
ids: [DSA-29]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Stable record sorting

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Stable merge sort orders records by a key while preserving the original order of equal keys.

## The story

Two support requests have the same priority. A sort moves the newer one ahead of the older one, even though the queue promises arrival order for ties.

## The idea in plain language

Recall [merging sorted arrays](../../day-005-merge-sorted-arrays/dsa_merge-sorted-arrays/CONCEPTS.md). Stability means equal-key records retain
their relative input order. Split an unsorted sequence into contiguous halves, sort each half,
then merge the two ordered streams. Contiguous splitting retains the information needed to
resolve ties: an equal record from the left half originally preceded one from the right.
Recognize this pattern when ordering needs a predictable tie policy or later passes must
preserve an earlier ordering. Comparing entire records can accidentally introduce a new tie rule.

## Why Krama needs it

This develops DSA-29. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Official LeetCode companion](https://leetcode.com/problems/sort-an-array/) defines the online contract; [LEETCODE.md](LEETCODE.md) compares it with local practice.
[Sorting Techniques](https://docs.python.org/3.12/howto/sorting.html) documents the stable library oracle.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

For records (name, score), use [(z,3),(b,1),(a,3),(c,2)]. The halves become
[(b,1),(z,3)] and [(c,2),(a,3)]. Merge b before c because 1<2, then compare z and a:
both scores are 3, so take z from the left. The result is b,c,z,a, retaining the two tied
records' original order. Choosing a lexicographically would violate this contract.

The merge invariant is that the output is a stable sorted prefix of both consumed streams.
The smaller head is safe because everything behind it is at least as large. On equality,
left-first preserves cross-half order; recursive stability preserves within-half order.
Empty and singleton runs are already sorted. Every level processes n records and the split
depth is O(log n), so time is O(n log n). A reusable merge buffer costs O(n), plus O(log n)
recursive stack. Slicing implementations allocate extra arrays; their peak live storage can
still be O(n), but total copying work and allocation traffic must be acknowledged.

The numeric online companion does not expose stability with distinguishable records. Implement
the merge mechanism without built-in sorting for that route; tagged equal scores are the local
test that detects instability. Library sorting is a useful oracle, not the assigned implementation.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
left, right = [('z', 3)], [('a', 3)]
wrong = right + left  # Taking the right record when keys tie.
fixed = left + right
print('wrong tie order:', [x[0] for x in wrong])
print('stable tie order:', [x[0] for x in fixed])
assert [x[1] for x in wrong] == [3, 3]  # Sortedness alone misses the bug.
assert fixed == sorted(left + right, key=lambda x: x[1])
assert wrong != fixed
```

**Line by line:** The two runs isolate the equality decision. Both outputs have sorted scores, but only left-first matches the stable oracle. The final inequality proves the test distinguishes the plausible bug.

Observed author output on Python 3.12.10, 2026-09-23:

```text
wrong tie order: ['a', 'z']
stable tie order: ['z', 'a']
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Use Python's stable key-based sort in ordinary application code unless this is an algorithm
exercise. Keep the key function free of changing external state. For inputs larger than memory,
external merge sorting creates sorted runs and merges them with bounded buffers; I/O dominates.
A reviewer should ask whether the tie order is part of the API and whether input mutation is
allowed. Optional follow-up: why can successive stable sorts implement multiple-key ordering?

## Check yourself

### Readiness before practice

1. Why does choosing the left head on equality preserve arrival order?
2. Can sorted scores alone prove stability?
3. Where does each factor in O(n log n) come from?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.
