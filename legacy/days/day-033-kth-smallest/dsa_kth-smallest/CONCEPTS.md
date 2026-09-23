---
day: 33
part: "1.1"
title: "Kth smallest"
ids: [DSA-33]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Kth smallest

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Quickselect partitions around a pivot and retains only the region containing the required rank.

## The story

A dashboard needs one percentile threshold, but a full sort spends work ordering every other value too.

## The idea in plain language

Recall [sorting](../../day-029-stable-record-sorting/dsa_stable-record-sorting/CONCEPTS.md) and [shrinking search bounds](../../day-022-lower-bound/dsa_lower-bound/CONCEPTS.md). A rank
is a position in sorted order, including repeated values. Partitioning groups values smaller
than, equal to, and larger than a pivot without sorting each group. Those group sizes tell
which group owns a requested rank. Equal values occupy multiple consecutive ranks.

## Why Krama needs it

This develops DSA-33. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Official LeetCode companion](https://leetcode.com/problems/kth-largest-element-in-an-array/) defines the online contract; [LEETCODE.md](LEETCODE.md) compares it with local practice.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

For [8,3,5,3,9,1] and one-based k=4, use zero-based target=3. Pivot 3 yields
less=[1], equal=[3,3], greater=[8,5,9]. Ranks 0, 1–2, and 3–5 belong to those groups.
Target 3 therefore becomes target 0 inside greater. Pivot 8 there gives [5], [8], [9];
target 0 is 5. A sorted oracle [1,3,3,5,8,9] confirms the result.

For an in-place three-way partition of [lo,hi), maintain [lo,lt)<pivot,
[lt,i)==pivot, [i,gt) unknown, and [gt,hi)>pivot. If a[i]<pivot, swap with a[lt] and
advance lt and i. If equal, advance i. If greater, decrease gt and swap with a[gt], leaving
i unchanged because the swapped-in value is unclassified. Once i==gt, compare the absolute
target index with lt and gt, then narrow to the needed side or return the pivot. A pivot
chosen from the current range guarantees a nonempty equal region and progress.

Random uniform pivots give expected O(n) total work, but worst-case O(n²) remains possible.
Always choosing an extreme on sorted distinct input produces n+(n-1)+... comparisons.
An iterative in-place partition uses O(1) auxiliary space; copying to preserve input costs
O(n), and allocating separate groups also costs O(n) peak space for an iterative version.
The online kth LARGEST target is n-k in ascending order; local kth SMALLEST uses k-1.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
values = [8, 3, 5, 3, 9, 1]
pivot = 3
less = [x for x in values if x < pivot]
equal = [x for x in values if x == pivot]
greater = [x for x in values if x > pivot]
print('partition:', less, equal, greater)
k = 2
wrong = sorted(set(values))[k - 1]
expected = sorted(values)[k - 1]
assert wrong == expected  # This weak case hides deduplication.
k = 3
wrong = sorted(set(values))[k - 1]
expected = sorted(values)[k - 1]
print('deduplicated rank:', wrong, 'actual rank:', expected)
assert wrong != expected and expected == 3
```

**Line by line:** Three comprehensions visualize the partition, not a full quickselect implementation. The second-rank test happens to pass after deduplication; the third-rank test exposes that repeated values consume ranks.

Observed author output on Python 3.12.10, 2026-09-23:

```text
partition: [1] [3, 3] [8, 5, 9]
deduplicated rank: 5 actual rank: 3
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

In an interview, name the pivot strategy and whether mutation is allowed before claiming
linear expected time. For adversarial input, randomization or an introspective fallback may
be preferable to a fixed pivot. Deterministic linear-time selection needs a stronger pivot
construction and belongs in optional depth. For a small k over a stream, a bounded heap has
different advantages; quickselect assumes access to the candidate collection.

## Check yourself

### Readiness before practice

1. Why must i stay still after swapping from the greater region?
2. Which ranks belong to three copies of the pivot?
3. How do local and online target indexes differ?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.
