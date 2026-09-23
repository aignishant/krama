---
day: 5
part: "1.1"
title: "Merge by choosing between the next two candidates"
ids: [DSA-05]
level: working
prerequisites: ["Scan invariants", "Sorted arrays and indices"]
failure: true
---

# Merge by choosing between the next two candidates

Core for both routes: read this explanation and its readiness check. For the online route,
continue to [merging into spare capacity](BACKWARD_MERGE.md). That second part is optional
for local practice. Choose one main attempt within the existing 60-minute DSA budget.

## One-line answer

Two sorted inputs let you find the next output value by comparing only their unconsumed heads.

## The story

Two reception desks each keep appointment cards in time order. To make one schedule, compare
the first remaining card from each desk. The earlier one must come next: every card behind
it at its own desk is at least as late. There is no need to sort all the cards again.

## The idea in plain language

**Nondecreasing** order allows ties: each value is at least the one before it. Merging combines
all occurrences from two already ordered inputs. It does not remove duplicates. Recognize this
pattern when joining ordered logs, sorted runs, or two lists using the same comparison key.

Recall [the invariant proof](../../day-001-count-target-values/dsa_count-target-values/CONCEPTS.md)
and [stability](../../day-003-stable-compaction/dsa_stable-compaction/CONCEPTS.md). Sortedness is
the assumption that makes considering only two candidates safe. If either input is unordered,
a smaller value may be hidden behind its head and the argument fails.

## Why Krama needs it

This connects two-pointer state to an ordering proof. Each pointer describes how much of one
input is consumed, while the output describes exactly what both consumed prefixes contribute.

## The mechanism

### Worked trace

Appointment times are A=`[2, 7, 7]` and B=`[3, 7, 9]`. Start i=j=0 and an empty output.
For a deterministic stable merge relative to A followed by B, take from A on equality.

| Heads compared | Source taken | New i, j | Output |
| --- | --- | --- | --- |
| 2 and 3 | A | 1, 0 | 2 |
| 7 and 3 | B | 1, 1 | 2, 3 |
| 7 and 7 | A | 2, 1 | 2, 3, 7 |
| 7 and 7 | A | 3, 1 | 2, 3, 7, 7 |
| A exhausted | Remaining B | 3, 3 | 2, 3, 7, 7, 7, 9 |

Before every comparison, the output is a sorted merge of A's first i and B's first j items,
and no remaining item is smaller than the output's last item. Initially this holds for empty
prefixes. Each input's head is its smallest remaining value, so the smaller head is the
smallest remaining value overall. Appending it and advancing only that source preserves the
invariant and consumes exactly one occurrence. On equal heads, emit one occurrence now; the
other still exists and must be emitted later.

When one input ends, its absence cannot be compared as a normal value. Append the other
input's remaining values in their existing order. They cannot be smaller than the output's
last value. This handles empty inputs naturally, including two empty inputs in the local task.
Termination follows because each emitted item reduces the number of unconsumed items.

For lengths n and m, every occurrence is emitted once: O(n+m) time under unit-cost comparisons.
The required new output uses O(n+m) space; two indices use O(1) auxiliary space excluding output.
Slicing the remaining suffix creates temporary storage, so an index-based tail loop supports
the strict constant-auxiliary claim. Repeated `pop(0)` shifts list contents and can make a
seemingly simple merge quadratic. Concatenate-and-sort is a useful independent baseline with
an O((n+m) log(n+m)) general sorting upper bound; it does not explain the two-head mechanism.

## When it breaks

This teaching fragment correctly merges until one desk runs out, then forgets the remaining cards.

```python
desk_a = [2, 8]
desk_b = [3]
i = j = 0
schedule = []
while i < len(desk_a) and j < len(desk_b):
    if desk_a[i] <= desk_b[j]:
        schedule.append(desk_a[i])
        i += 1
    else:
        schedule.append(desk_b[j])
        j += 1
print("before cleanup:", schedule)
try:
    assert len(schedule) == len(desk_a) + len(desk_b), "an unconsumed tail was lost"
except AssertionError as error:
    print(f"AssertionError: {error}")
while i < len(desk_a):
    schedule.append(desk_a[i])
    i += 1
while j < len(desk_b):
    schedule.append(desk_b[j])
    j += 1
assert schedule == [2, 3, 8]
print("after cleanup:", schedule)
```

**Line by line:** the two indices start at their respective heads. The main loop requires both
heads to exist, appends one selected card, and advances its source. The length assertion catches
the missing occurrence. Each cleanup loop consumes only its own remaining suffix; at most one
has work. The final assertion checks actual order as well as completeness. This appointment
fixture teaches the mechanism; implement the assignment adapter independently.

Author verification on Python 3.12.10, 2026-09-22:

```text
before cleanup: [2, 3]
AssertionError: an unconsumed tail was lost
after cleanup: [2, 3, 8]
```

## In production

Require a common sort key and compatible ordering from both producers. With labelled records,
tie handling affects reproducibility even when numeric examples look identical. A streaming
merge can retain only current heads, but output storage and consumer buffering still need their
own accounting. If inputs share storage with the destination, forward writes need a separate
safety proof: read [the backward-merge lesson](BACKWARD_MERGE.md) for today's online variation.

## Check yourself

### Readiness before practice

1. Why can neither hidden suffix contain a smaller candidate than its head?
2. What happens to both occurrences when the heads are equal?
3. What work remains when the comparison loop ends?
4. Why is O(1) auxiliary space compatible with O(n+m) output space here?

Then choose [local practice](PRACTICE.md), or read [backward merging](BACKWARD_MERGE.md)
before [LeetCode practice](LEETCODE.md). Locally run `python course.py practice 5` after your
implementation. Include empty inputs, an exhausted short side, interleaving, negatives, and
equal values. Check length, multiplicity, ordering, and that the result is a new list, even
when one input is empty. Record actual evidence in [NOTES.md](NOTES.md).

Optional depth: label equal-key records to test stability, or model a merge of two iterators.

[Navigation](README.md) · [Quick recall](../../../docs/DSA_RECALL.md#day-005-merge-sorted-arrays)
