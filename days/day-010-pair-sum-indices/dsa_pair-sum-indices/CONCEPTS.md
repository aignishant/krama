---
day: 10
part: "1.1"
title: "Remember complements without losing index order"
ids: [DSA-10]
level: working
prerequisites: ["Hash membership", "Prefix invariants"]
failure: true
---

# Remember complements without losing index order

Core: complement lookup, distinct indices, and the local ordering rule. Alternative representations
and production numeric domains are optional depth.

## One-line answer

Look for the needed partner among earlier values, retaining the earliest index and the best complete pair.

## The story

Two purchases must total a fixed allowance. Finding any matching pair is enough for one receipt
checker; another requires the earliest first receipt, then the earliest second receipt. The first
pair discovered while scanning second receipts need not satisfy that second rule.

## The idea in plain language

If the current value is x, its complement is target minus x. Searching for that one value
replaces comparing x with every earlier value. Recall [membership](../../day-008-first-repeated-value/dsa_first-repeated-value/CONCEPTS.md).
Today the remembered table must retain an index, because the answer identifies positions.

Lexicographic order compares first indices first, then second indices when the first are equal.
Thus `[0, 3]` is smaller than `[1, 2]`. A correct baseline enumerates every pair i < j and takes
the smallest qualifying pair: O(n²) time and O(1) working state beyond the fixed-size answer.
Recognize complement lookup when one term of an equation determines the exact other term.

## Why Krama needs it

[Count target subarrays](../../day-013-count-target-subarrays/dsa_count-target-subarrays/README.md)
will turn a sum equation into a lookup of a previously observed total. What the table stores
must still match the output: an index here, a count there.

## The source behind it

[Two Sum](https://leetcode.com/problems/two-sum/) (`spec:leetcode-1`, checked 2026-09-22)
guarantees exactly one solution with distinct positions and accepts either index order.
Local practice permits zero or many answers and requires the lexicographically smallest pair.

## The mechanism

### Worked trace

Use `[4, 1, 5, 2]`, target 6. The table contains earliest indices strictly before j.

| j | Value | Needed | Earlier partner | Best after comparison |
| --- | --- | --- | --- | --- |
| 0 | 4 | 2 | None | None |
| 1 | 1 | 5 | None | None |
| 2 | 5 | 1 | Index 1 | `[1, 2]` |
| 3 | 2 | 4 | Index 0 | `[0, 3]` |

Check the complement before inserting the current index. That guarantees i < j, including
when the two values are equal. A lone 3 cannot pair with itself for target 6; `[3, 3]` can.
Insert an index only when its value is absent. Replacing an earlier index by a later duplicate
can only worsen a future pair's first component.

For a fixed j, the earliest matching i dominates all other matching indices. Compare that
candidate with the current best pair, then continue. Every valid pair has some right endpoint;
when that endpoint is visited, the best possible left endpoint for it is considered. Keeping
the smallest of those candidates therefore yields the globally smallest pair. Exhaustion with
no candidate returns `[]`. An index of zero is valid: test membership, not the truthiness of a
retrieved index.

Expected time is O(n), auxiliary space O(u) for u distinct values, and output O(1), under the
usual integer hashing model. Collision-heavy hashing can degrade the time bound. Sorting the
values requires preserving original indices and still handling the ordering rule; it is not
a free substitute for the table.

## When it breaks

```python
values = [4, 1, 5, 2]
target = 6
candidates = [(i, j) for j in range(len(values))
              for i in range(j) if values[i] + values[j] == target]
print("discovery order:", candidates)
print("smallest pair:", min(candidates))
try:
    assert candidates[0] == min(candidates), "first match minimizes the wrong index"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert min(candidates) == (0, 3)
```

**Line by line:** this deliberately simple oracle enumerates pairs by increasing right endpoint.
`range(j)` excludes self-pairs. The filter accepts only the target sum. Taking the first candidate
models premature return; `min` compares tuples by the actual contract. The counterexample is
checked independently of a hash implementation. This teaching oracle uses O(n²) time and can
store O(n²) candidates; those are not the optimized algorithm's bounds.

Author verification on Python 3.12.10, 2026-09-22:

```text
discovery order: [(1, 2), (0, 3)]
smallest pair: (0, 3)
AssertionError: first match minimizes the wrong index
```

## In production

Specify numeric semantics before using exact complements: integer minor units suit many exact
counting tasks, whereas floating-point rounding changes equality. Validate domains at boundaries.
A reviewer should ask whether duplicate values represent different records and whether the API
promises any pair or a deterministic one. If data arrives forever, an exact all-history table
has no fixed memory ceiling. Eviction changes which historical pairs remain discoverable.

## Check yourself

### Readiness before practice

1. Why does `[4, 1, 5, 2]` defeat returning the first local match?
2. Which index should be retained for repeated values, and why?
3. How does lookup before insertion handle a repeated half-target?
4. Which guarantee makes early return safe in the online problem?

Run the oracle block and explain the dominance argument aloud. Then choose [PRACTICE.md](PRACTICE.md)
or [LEETCODE.md](LEETCODE.md); test no answer, duplicate partners, index zero, and competing pairs.

[Navigation](README.md) · [Recall](../../../docs/DSA_RECALL.md#day-010-pair-sum-indices)
