---
day: 13
part: "1.1"
title: "Count earlier prefix boundaries"
ids: [DSA-13]
level: working
prerequisites: ["Day 12 prefix sums", "Frequency dictionaries"]
failure: true
---

# Count earlier prefix boundaries

Core: explanation, worked trace, and readiness. Production extensions are optional depth;
continue another sitting if needed within the existing track budget.

## One-line answer

For each right boundary, count earlier prefixes equal to the current total minus the target.

## The story

A receipt report asks how many consecutive runs total the same amount. Refunds can lower the running total, so stopping when a sum becomes too large can miss a later match.

## The idea in plain language

A subarray is a consecutive, nonempty interval. A prefix total P[t] sums the first t values;
[Day 12](../../day-012-range-sums/dsa_range-sums/CONCEPTS.md) explains this boundary convention.
The interval from boundary l to boundary r has sum P[r] - P[l]. Rearranging the equation for
target k gives P[l] = P[r] - k. A frequency dictionary stores how many earlier boundaries had
each total. It retains multiplicity, unlike a set, because equal totals at different boundaries
identify different intervals. Recognize this technique when counting target sums with signed
values; a window that shrinks whenever its sum is too large has no monotonic guarantee.

## Why Krama needs it

The [Week 2 review](../../day-014-week-2-review/dsa_week-2-dsa-review/README.md) asks you to distinguish membership, counts, indices, and prefix boundaries.

## The source behind it

[Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) (LeetCode 560) defines the same nonempty contiguous-sum count. The local input is a JSON object with nums and k. Checked 2026-09-22; see the dated [source ledger](../../../docs/SOURCES.md).

## The mechanism

### Worked trace

For `[2, -2, 2]`, target 2, seed the dictionary with `{0: 1}` for the empty prefix.

| Right boundary | Current total | Needed earlier total | Matches before insert | Running answer |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 1 | 1 |
| 2 | 0 | -2 | 0 | 1 |
| 3 | 2 | 0 | 2 | 3 |

After querying, increment the frequency of the current total. Before each query the dictionary
contains exactly boundaries strictly earlier than r. Every matching boundary produces one
nonempty valid interval, and every valid interval is counted at its unique right boundary.
The empty prefix permits intervals starting at index zero; it is not an empty subarray answer.

A baseline extends a running sum from every start: O(n²) time and O(1) auxiliary space.
The frequency method uses expected O(n) time and O(n) auxiliary space with ordinary hash-table
assumptions. It needs no full prefix array. All-zero input has n(n+1)/2 matches, so the answer
can be much larger than n. Python large-integer arithmetic is not constant cost without the
usual interview unit-cost assumption.

## When it breaks

```python
prefixes = [0, 0, 0]  # two zeros have three prefix boundaries
frequency = {0: 1}
correct = wrong = 0
for total in prefixes[1:]:
    correct += frequency.get(total, 0)
    frequency[total] = frequency.get(total, 0) + 1
    wrong += frequency[total]
print("query first:", correct, "insert first:", wrong)
try:
    assert wrong == correct, "current boundary counted as an empty interval"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert correct == 3
```

**Line by line:** The list supplies already-computed boundaries to isolate update order. The initial frequency represents boundary zero. Querying before incrementing counts only earlier boundaries. The wrong accumulator queries after incrementing, adding one empty interval per step.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
query first: 3 insert first: 5
AssertionError: current boundary counted as an empty interval
```

A set would count only two matches in this example and lose one valid start. With `[3, -1]`
and target 2, discarding 3 when the running sum exceeds 2 loses the whole valid interval.

## In production

A long stream can grow the dictionary without bound. A retention window changes the contract and requires removing expired prefix counts. For one target the online state suffices; many arbitrary targets may require different preprocessing. Review both memory growth and integer range before calling the scan constant space.

## Check yourself

### Readiness before practice

1. Why is zero seeded once?
2. What does each of the two zero-prefix occurrences represent in the trace?
3. Why must lookup precede insertion when k is zero?
4. Which signed input disproves a shrink-on-excess window?

Run the teaching block in a scratch interpreter, then explain the distinguishing failure aloud.
Use [README.md](README.md) to enter the assignment and record your own evidence.
