---
day: 7
part: "1.1"
title: "Review the invariant instead of memorizing the loop"
ids: [DSA-07]
level: working
prerequisites: ["Days 1–6 DSA attempts"]
failure: true
---

# Review the invariant instead of memorizing the loop

**Cold assessment first:** attempt the two problems in [the weekly assessment](PRACTICE.md#weekly-assessment)
before reading this repair lesson or its examples. Opening it earlier is guided practice;
record that help and schedule another cold attempt. This review adds no new problem quota.

## One-line answer

Recall what each piece of state guarantees, then use counterexamples to test whether your code keeps that guarantee.

## The story

You sort receipts into a folder and check that the dates increase. One receipt has disappeared,
but the remaining dates still increase. A tidy-looking result is not enough to prove the job is done.

## The idea in plain language

A correctness explanation joins the exact contract to the maintained state. A regression test
is a check that detects a particular mistake if it returns. A cold attempt begins without
notes, old code, hints, or the reference. Familiarity with yesterday's code can hide a missing
reason for why its update works.

Recognize that gap when you can write a loop but cannot say why a boundary is safe or why ties
take a particular branch. Repair the mechanism that failed, then close the material and try again.

## Why Krama needs it

[Day 8](../../day-008-first-repeated-value/dsa_first-repeated-value/CONCEPTS.md) replaces scalar
state with a set. The same questions remain: what does the state represent, when do you update
it, and why is the first reported answer the right one?

## The source behind it

This is an original assessment method using the prior lessons. The online review contracts are
[How Many Numbers Are Smaller Than the Current Number](https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/)
(`spec:leetcode-1365`) and [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/)
(`spec:leetcode-88`), rechecked 2026-09-22. They differ from the local counting and fresh-output
merge exercises; use [LEETCODE.md](LEETCODE.md) to choose the correct interface.

## The mechanism

### Worked trace

Use this map only after the cold attempts. Follow the link for the mechanism you could not defend.

| Earlier lesson | State to reconstruct | Mistake that challenges it |
| --- | --- | --- |
| [Count](../../day-001-count-target-values/dsa_count-target-values/CONCEPTS.md) | Number of matches in the processed prefix | Reset on a nonmatch |
| [First maximum](../../day-002-find-the-first-maximum/dsa_find-the-first-maximum/CONCEPTS.md) | Earliest maximum's index | Replace on equality |
| [Compaction](../../day-003-stable-compaction/dsa_stable-compaction/CONCEPTS.md) | Kept prefix; write never ahead of read | Overwrite unread items |
| [Reverse](../../day-004-reverse-a-segment/dsa_reverse-a-segment/CONCEPTS.md) | Final outside region; unprocessed interior | Confuse an exclusive endpoint with an included index |
| [Merge](../../day-005-merge-sorted-arrays/dsa_merge-sorted-arrays/CONCEPTS.md) | Sorted output containing every consumed occurrence | Lose duplicates or a remaining tail |
| [Trade](../../day-006-best-single-trade/dsa_best-single-trade/CONCEPTS.md) | Cheapest eligible past price and best completed profit | Ignore chronology |

Consider merging teaching inputs `[1, 4]` and `[1, 3]`. Taking the left 1 produces `[1]`;
the right 1 remains unread. Taking it produces `[1, 1]`, followed by 3 and the remaining 4.
At every step, output length equals the total number of consumed items. Sortedness alone
misses the difference between `[1, 3, 4]` and the required `[1, 1, 3, 4]`.

Check initialization, one update, and termination aloud. Then separate time, auxiliary space,
and output space. Local merge has O(n+m) time and O(n+m) required output; two indices need
O(1) extra state if you avoid temporary slices. For the online route, repair
[backward merging](../../day-005-merge-sorted-arrays/dsa_merge-sorted-arrays/BACKWARD_MERGE.md).
For the online counting route, repair
[frequency and cumulative counts](../../day-001-count-target-values/dsa_count-target-values/FREQUENCY_COUNTS.md).

## When it breaks

```python
left, right = [1, 4], [1, 3]
wrong = sorted(set(left + right))
assert wrong == sorted(wrong)
print("sortedness-only check: PASS", wrong)
try:
    assert len(wrong) == len(left) + len(right), "one occurrence disappeared"
except AssertionError as error:
    print(f"AssertionError: {error}")
oracle = sorted(left + right)
assert oracle == [1, 1, 3, 4]
print("multiplicity-aware oracle:", oracle)
```

**Line by line:** converting to a set deliberately drops multiplicity. The first assertion
still passes, demonstrating a weak check. The length assertion catches this fixture's defect;
it is not sufficient by itself to prove all values are correct. Sorting concatenated small
inputs provides an independent value oracle, at O((n+m) log(n+m)) time and O(n+m) storage.

Author verification on Python 3.12.10, 2026-09-22:

```text
sortedness-only check: PASS [1, 3, 4]
AssertionError: one occurrence disappeared
multiplicity-aware oracle: [1, 1, 3, 4]
```

## In production

Use an independent oracle only at sizes where its cost is acceptable. Random inputs supplement
boundary cases, not replace them. Record the seed, exact failing input, and test command so a
failure can be reproduced. Assertions that only repeat implementation choices can miss the
same bug. A useful review comment asks which wrong implementation the test would reject.

Two completed cold re-solves, tests, and explanations are the weekly gate. Score each attempt
for correctness, explanation, complexity, and tests, each 0–2; require 6/8 with correctness=2
and at least one hint-free solve. A hard unresolved problem may replace the second attempt;
if unfinished, record partial and continue later. Reading this lesson does not pass that gate.

## Check yourself

### Readiness after repair

1. Can you explain the retained state without naming loop variables?
2. What fixture distinguishes sorted output from a correct merge?
3. Which online routes require a different mechanism from their local counterparts?

Run the demonstration after your cold attempt. Explain why the first passing assertion was
insufficient. Use [NOTES.md](NOTES.md) to record both attempts, scores, help, and the next
cold review. Keep 5 recall + 20 first solve + 20 second solve + 10 critique + 5 log minutes.

[Navigation](README.md) · [Quick recall](../../../docs/DSA_RECALL.md#day-007-week-1-dsa-review)
