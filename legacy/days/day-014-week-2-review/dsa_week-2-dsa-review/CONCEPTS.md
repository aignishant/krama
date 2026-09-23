---
day: 14
part: "1.1"
title: "Review representations rather than memorized loops"
ids: [DSA-14]
level: working
prerequisites: ["Days 8\u201313"]
failure: true
---

# Review representations rather than memorized loops

Begin with the cold assignment in [README.md](README.md). Read this repair lesson only after
the attempt, or record that you deliberately used help.

Core: explanation, worked trace, and readiness. Production extensions are optional depth;
continue another sitting if needed within the existing track budget.

## One-line answer

Choose the smallest state that preserves the exact answer, then prove what that state means before every update.

## The story

A solution passes the sample but returns true where the task asks for the first repeated value. The algorithm recognized a broad pattern and forgot the actual output contract.

## The idea in plain language

A review tests retrieval before repair. Do the two assigned cold attempts first. Then use
the representation table to diagnose the gap: membership records existence, frequencies retain
multiplicity, index maps retain positions, canonical keys define equivalence, and prefix sums
retain cumulative boundaries. These structures answer different questions even when each uses
a dictionary or list. Correctness depends on the meaning of the state, not its container name.

## Why Krama needs it

[Day 15](../../day-015-sorted-pair-existence/dsa_sorted-pair-existence/CONCEPTS.md) changes the input assumption to sorted order, which changes which state is necessary.

## The source behind it

[Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) (217) and [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) (303) are the two online review companions. Checked 2026-09-22; see the dated [source ledger](../../../docs/SOURCES.md).

## The mechanism

### Worked trace

| Prior lesson | Information that must survive | Repair reading |
| --- | --- | --- |
| First repetition | Values seen strictly earlier; traversal order | [Day 8](../../day-008-first-repeated-value/dsa_first-repeated-value/CONCEPTS.md) |
| Frequency ranking | Counts plus declared tie order | [Day 9](../../day-009-frequency-ranking/dsa_frequency-ranking/CONCEPTS.md) |
| Pair indices | A compatible earlier index, respecting tie rules | [Day 10](../../day-010-pair-sum-indices/dsa_pair-sum-indices/CONCEPTS.md) |
| Anagrams | Canonical character multiplicities | [Day 11](../../day-011-group-anagrams/dsa_group-anagrams/CONCEPTS.md) |
| Range sums | Sum before each boundary | [Day 12](../../day-012-range-sums/dsa_range-sums/CONCEPTS.md) |
| Target subarrays | Frequencies of earlier prefix totals | [Day 13](../../day-013-count-target-subarrays/dsa_count-target-subarrays/CONCEPTS.md) |

Trace `[4, 9, 4]`: before the last item the seen set contains 4 and 9; querying first detects
the repetition of 4. Online returns True, while local Day 8 returns 4. Inserting before querying
would report every first occurrence as repeated. For range values `[4, -1, 3]`, prefix boundaries
are `[0, 4, 3, 6]`; query [1,2] subtracts P[1] from P[3], returning 2.

The two invariants explain the expected O(n) duplicate scan and O(n+q) batch query cost;
each needs O(n) auxiliary space in the worst case. Use the review's 5/20/20/10/5-minute
allocation, with tests and explanation inside each attempt window. If unfinished, record
partial rather than shrinking the required two-solve gate.

## When it breaks

```python
values = [4, -1, 3]
prefix = [0, 4, 3, 6]
left, right = 1, 2
wrong = prefix[right] - prefix[left]
correct = prefix[right + 1] - prefix[left]
print("excluded right:", wrong, "inclusive:", correct)
try:
    assert wrong == sum(values[left:right + 1]), "range endpoint lost"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert correct == 2
```

**Line by line:** The supplied prefix array isolates boundary interpretation. right denotes an included element, so right+1 selects the sum after it. The independent slice sum catches the missing endpoint.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
excluded right: -1 inclusive: 2
AssertionError: range endpoint lost
```

## In production

Separate a wrong algorithm from a wrong adapter: both can fail a service or interview. Reusable query objects must rebuild or update state after mutations. Record the smallest counterexample and exact mistaken assumption so a later review tests understanding rather than recognition of the same sample.

## Check yourself

### Readiness before practice

1. Explain why a set cannot replace a frequency map for Day 13.
2. Which online/local return contracts differ today?
3. Derive the inclusive query formula from boundary meanings.
4. Which regression would fail before your repair?

Run the teaching block in a scratch interpreter, then explain the distinguishing failure aloud.
Use [README.md](README.md) to enter the assignment and record your own evidence.
