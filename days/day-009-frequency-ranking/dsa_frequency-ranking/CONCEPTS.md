---
day: 9
part: "1.1"
title: "Count once, then rank distinct values"
ids: [DSA-09]
level: working
prerequisites: ["Frequency tables", "Set membership"]
failure: true
---

# Count once, then rank distinct values

Core for both routes: counting and ranking. The online route also needs the frequency-bucket
section below. Heap selection and unbounded streams are optional depth, within a later sitting.

## One-line answer

Summarize each value's frequency once, then order the distinct values using the required tie rule.

## The story

A shop lists its most requested item codes. Code 8 arrived first, but code 2 was requested just
as often. If ties must favor smaller codes, arrival order cannot decide the display order.

## The idea in plain language

Recall [frequency tables](../../day-001-count-target-values/dsa_count-target-values/FREQUENCY_COUNTS.md):
each distinct value has a count. Unlike [yesterday's set](../../day-008-first-repeated-value/dsa_first-repeated-value/CONCEPTS.md),
the table preserves multiplicity. It discards individual positions because ranking does not need them.

Recognize this pattern when the answer depends on how often values occur, rather than where they
occur. Separate two decisions: collecting counts and ordering the resulting records. A baseline
rescans the input to count each distinct value, doing O(nu) work for n inputs and u distinct values.
One pass can reuse those counts instead.

## Why Krama needs it

[Group anagrams](../../day-011-group-anagrams/dsa_group-anagrams/CONCEPTS.md) will preserve letter
multiplicity inside a key. Today's lesson makes explicit why presence alone loses information.

## The source behind it

[Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)
(`spec:leetcode-347`, checked 2026-09-22) asks for k frequent values with arbitrary output order
and a unique answer; its follow-up asks for better than O(n log n) time. Our local task instead
ranks every distinct integer and resolves equal frequencies by ascending value.

## The mechanism

### Worked trace

For `[8, 2, 8, 5, 2, 2, 5]`:

| Processed input | Count changed | Meaning |
| --- | --- | --- |
| 8 | 8 → 1 | One occurrence of 8 |
| 8, 2 | 2 → 1 | One occurrence of each |
| 8, 2, 8 | 8 → 2 | Reuse the previous count |
| Entire input | 8 → 2, 2 → 3, 5 → 2 | Every occurrence counted once |

Before each update the table counts exactly the processed prefix. Increasing only the current
value's count maintains that invariant. After the scan it contains the true frequencies.

To rank, give each value the key `(-frequency, value)`. Tuple comparison examines the first
component first and the second only on a tie. Negation makes greater counts sort earlier;
the unmodified value makes smaller values win ties. The keys are 8: `(-2, 8)`, 2: `(-3, 2)`,
5: `(-2, 5)`, giving `[2, 5, 8]`. Sorting by count alone cannot guarantee the local tie rule.

Expected counting time is O(n) under ordinary integer hashing. Sorting u keys costs
O(u log u), so total time is O(n + u log u), auxiliary space O(u), and output space O(u).
The practice brief calls the distinct count k; here u avoids confusing it with online top-k.
Empty local input naturally produces `[]`. A single distinct value appears once in the result.

### Online route: select by frequency buckets

A frequency is an integer between 1 and n. Create n+1 buckets, with bucket f containing values
whose count is f. In the example, bucket 3 holds `[2]` and bucket 2 holds `[8, 5]`; the other
positive buckets are empty. Visit buckets from n down to 1 and emit values until k are collected.
Every value in a later bucket has a lower count, so it cannot displace an earlier selection.
The unique-answer guarantee removes ambiguity across the cutoff for valid online inputs.

Counting, distributing u values, and scanning n bucket positions take expected O(n + u) time
and O(n + u) auxiliary space. Output needs O(k). No numeric tie sorting is required online.
This teaches the extra mechanism needed for the follow-up; simply sorting all distinct values
does not beat O(n log n) when u grows with n. A size-k heap is an optional alternative with
O(u log k) selection work after counting, useful when n-sized bucket storage is unattractive.

## When it breaks

```python
counts = {8: 2, 2: 3, 5: 2}
wrong = sorted(counts, key=lambda value: -counts[value])
right = sorted(counts, key=lambda value: (-counts[value], value))
print("count only:", wrong)
print("explicit ties:", right)
try:
    assert wrong == [2, 5, 8], "equal counts still need a value tie-break"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert right == [2, 5, 8]
```

**Line by line:** the dictionary is a completed teaching count table. The first key ignores
value, preserving insertion order among equal keys. The tuple key explicitly resolves ties.
The caught assertion exposes the incomplete key; the final assertion checks the repair.

Author verification on Python 3.12.10, 2026-09-22:

```text
count only: [2, 8, 5]
explicit ties: [2, 5, 8]
AssertionError: equal counts still need a value tie-break
```

## In production

Exact counts for an unbounded stream grow with the number of distinct keys. Define a window
or use an explicitly approximate method if memory must be bounded. Neither silently preserves
the original all-history contract. Adversarial hash collisions can invalidate expected linear
counting time; large integers and expensive equality add costs beyond the unit-cost model.
A reviewer should ask whether deterministic ordering is part of the API and whether ties at
a top-k cutoff should include more than k records. Those are product decisions, not syntax.

## Check yourself

### Readiness before practice

1. Why is a set insufficient, and why are original indices unnecessary?
2. What order follows from counts `{4: 2, 1: 2, 9: 3}`?
3. Why can buckets avoid comparison sorting for the online follow-up?
4. Which memory and tie guarantees change between the two routes?

Run the teaching block in a scratch Python session. Explain the count invariant aloud, then
choose [local practice](PRACTICE.md) or [LeetCode](LEETCODE.md) within the same hour.

[Navigation](README.md) · [Recall](../../../docs/DSA_RECALL.md#day-009-frequency-ranking)
