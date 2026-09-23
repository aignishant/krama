---
day: 34
part: "1.1"
title: "Count inversions"
ids: [DSA-34]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Count inversions

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Count inversions during merging by charging each smaller right value for all remaining larger left values.

## The story

A report compares the order of two event streams. Checking every earlier event against every later event becomes slow long before the data stops fitting in memory.

## The idea in plain language

Prerequisite: [merge sort](../../day-029-stable-record-sorting/dsa_stable-record-sorting/CONCEPTS.md). An inversion is a pair of positions i<j
whose values satisfy a[i]>a[j]. Splitting by original position separates pairs into left-only,
right-only, and cross-half pairs. Recursion counts the first two; sorted halves let one merge
step count many cross pairs at once. Equal values are not ordinary inversions.

## Why Krama needs it

This develops DSA-34. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Official LeetCode companion](https://leetcode.com/problems/reverse-pairs/) defines the online contract; [LEETCODE.md](LEETCODE.md) compares it with local practice.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

Take original [4,7,2,5]. The halves [4,7] and [2,5] already have zero internal inversions.
During merge, right head 2 is below left head 4, so it forms two inversions with [4,7].
Then take 4. Right head 5 is below remaining 7, contributing one. The sorted merged result
is [2,4,5,7], with 3 inversions: (4,2),(7,2),(7,5).

Whenever right[j]<left[i], every left element at i or later is larger, so add len(left)-i.
Every cross pair is charged once when its right element is consumed. Choosing left on equality
avoids counting equal values. Recurrence T(n)=2T(n/2)+O(n) gives O(n log n), with O(n) merge
storage and O(log n) stack. The count itself can reach n(n-1)/2; Python integers grow as needed.

### Online variation: reverse pairs

The online predicate is left[i]>2*right[j]. Ordinary merge ordering cannot count these by
simply replacing its comparison: it would stop producing sorted halves. Instead count cross
pairs in a SEPARATE pass before the normal merge. For each left value in ascending order,
advance j while left_value>2*right[j], adding j (for a zero-based right half). j never retreats
because increasing left values cannot invalidate previously qualifying right values. Then
merge by ordinary <=. Each level remains linear. Negative values still work because multiplying
by positive 2 preserves order; [-3,-2] contains zero ordinary inversions but one reverse pair.
Keep both predicates and their tests distinct. The extra pass is required reading for the online route.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
left, right = [4, 7], [2, 5]
ordinary = sum(a > b for a in left for b in right)
reverse = sum(a > 2*b for a in left for b in right)
j = count = 0
for a in left:
    while j < len(right) and a > 2*right[j]:
        j += 1
    count += j
print('ordinary cross pairs:', ordinary)
print('reverse cross pairs:', reverse, 'monotone pass:', count)
assert ordinary == 3 and reverse == count == 1
print('negative pair:', -3 > -2, -3 > 2*(-2))
assert not (-3 > -2) and -3 > 2*(-2)
```

**Line by line:** The nested sums are tiny-input oracles for two different predicates. The moving j counts a qualifying prefix of the sorted right half for each left value. The negative example rejects the assumption that a reverse pair must first be an ordinary inversion.

Observed author output on Python 3.12.10, 2026-09-23:

```text
ordinary cross pairs: 3
reverse cross pairs: 1 monotone pass: 1
negative pair: False True
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Use a wide enough counter in fixed-width languages and avoid overflow in doubling values.
For incremental events, a rank-count structure may be more suitable than repeatedly sorting
history. Review whether the input must survive unchanged and whether equal events count as
disorder. Optional depth: compare random tiny arrays with the pairwise oracle for both
predicates, especially duplicates and negatives; passing one predicate does not validate the other.

## Check yourself

### Readiness before practice

1. Why add the number of remaining left values rather than one?
2. Why must reverse-pair counting be separate from merging?
3. What does [-3,-2] reveal?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.
