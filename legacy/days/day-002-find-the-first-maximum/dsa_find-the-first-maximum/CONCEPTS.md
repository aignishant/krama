---
day: 2
part: "1.1"
title: "Keep the earliest best candidate"
ids: [DSA-02]
level: foundation
prerequisites: ["Day 1 scan invariants"]
failure: true
---

# Keep the earliest best candidate

Core for either route: read this lesson, trace the candidate, then check readiness. The online
route also needs [dominance checks](DOMINANCE.md); that part is optional for local practice.
Use the existing concept window; continue reading in another sitting if needed.

## One-line answer

A maximum scan keeps the best value seen so far and enough information to honor the tie rule.

## The story

You compare prices offered for a used desk. Two buyers offer the same highest price, and you
promised the desk to whoever offered that price first. Writing down only the price loses the
identity of the buyer. Replacing the name on an equal offer breaks your promise.

## The idea in plain language

Start with [Day 1's contract and invariant](../../day-001-count-target-values/dsa_count-target-values/CONCEPTS.md).
The requested answer is a position, not a value. Retain a candidate index; the input at that
index supplies its value. A later candidate replaces it only if the later value is strictly
larger. The equality decision is part of correctness, not an incidental coding preference.

Recognize this pattern when one best item is required from an unordered collection and each
item can be compared independently. A top-three request needs more state; finding all ties
needs output storage. Sorting organizes more information than a single maximum query needs.

## Why Krama needs it

This is the first scan where initialization and equality policy matter as much as the update.
Later windows and greedy choices reuse the question: what can safely replace the saved answer?

## The mechanism

### Worked trace

Teaching offers are `[4, 9, 6, 9]`, with positions starting at zero.

| Processed positions | New offer | Candidate index | Reason |
| --- | --- | --- | --- |
| 0 | 4 | 0 | First actual offer establishes a valid candidate |
| 0–1 | 9 | 1 | Strict improvement over 4 |
| 0–2 | 6 | 1 | Smaller offers cannot win |
| 0–3 | 9 | 1 | Equal value keeps the earlier offer |

Before examining position i, the candidate is the earliest maximum of positions 0 through i−1.
Initialization establishes this for the first element. A larger value becomes the unique best
of the extended prefix. A smaller value cannot win; an equal value cannot beat the earlier
position. Thus both keeping and replacing preserve the invariant. After the last comparison,
the prefix is the whole collection.

An empty collection has no first candidate. Handle its specified no-answer result before
accessing position zero. Do not initialize the best value to zero: zero may not occur, and
every valid input value may be negative. An actual first element works without a numeric sentinel.

### Cost and limits

For n nonempty items, there are n−1 comparisons: O(n) time and O(1) auxiliary space under the
unit-cost model. Returning an index adds constant output space. A loop over `nums[1:]` silently
allocates a slice; iterate indices or an iterator if claiming constant auxiliary space.
Any unseen value could be larger, so an exact general scan cannot stop early without additional
constraints. Assume ordinarily ordered integers; special comparison rules need a new contract.

## When it breaks

This deliberately wrong demonstration finds the **cheapest** quote but replaces the earliest
supplier on ties. It transfers the same reasoning to a different task from your assignment.

```python
quotes = [8, 3, 3]
chosen = 0
for index in range(1, len(quotes)):
    if quotes[index] <= quotes[chosen]:
        chosen = index
print("chosen:", chosen)
try:
    assert chosen == 1, "equal quote displaced the first supplier"
except AssertionError as error:
    print(f"AssertionError: {error}")

chosen = 0
for index in range(1, len(quotes)):
    if quotes[index] < quotes[chosen]:
        chosen = index
assert chosen == 1
print("strict comparison:", chosen)
```

**Line by line:** the first quote supplies an actual candidate. `range(1, len(quotes))` visits
only the remaining positions. `<=` lets a tied later supplier overwrite the answer. The assertion
checks identity through its index, not just the minimum price. The second scan changes only the
comparison, and its assertion verifies the repaired tie policy.

Author verification on Python 3.12.10, 2026-09-22:

```text
chosen: 2
AssertionError: equal quote displaced the first supplier
strict comparison: 1
```

A test with distinct values misses this bug. Two equal best values are the distinguishing case.

## In production

Make ranking and tie rules explicit for bids, monitoring peaks, or selected records. Do not
silently sort a caller's data to answer a query. If records arrive as a stream, retain the
candidate value and its sequence number because previous records may no longer be available.
Review question: can a refactor change which equally ranked record wins?

## Check yourself

### Readiness before practice

1. Trace `[-8, -2, -2, -6]`. Which index survives, and why?
2. Why is zero an unsafe initial best value but position zero safe for nonempty input?
3. What changes when the contract requests the last maximum?
4. Why do you need both a tie case and an empty case?

You are ready when you can explain initialization, equality, and termination without code.
For local practice, open [the contract](PRACTICE.md), implement independently, then run
`python course.py practice 2`. Include empty, singleton, all-negative, tied-best, and last-best
cases across your checks; the starter sample alone is insufficient.

For online practice, continue to [dominance checks](DOMINANCE.md) first. Record your own
reasoning and actual results in [NOTES.md](NOTES.md). Optional follow-up: return every tied
position and account for the additional output memory.

[Back to navigation](README.md) · [Quick recall](../../../docs/DSA_RECALL.md#day-002-first-maximum-and-dominance)
