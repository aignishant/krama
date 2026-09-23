---
day: 1
part: "1.2"
title: "Reuse counts across many questions"
ids: [DSA-01]
level: working
prerequisites: ["CONCEPTS.md: predicates, scans, and invariants"]
sources: ["spec:leetcode-1365"]
failure: true
---

# Reuse counts across many questions

Read this after [the counting introduction](CONCEPTS.md), before the online companion.
For the local single-target exercise, this is optional depth. The teaching example is a set
of independent inventory queries, so you still implement the assigned problem yourself.

## One-line answer

When many questions use the same data, summarize repeated values once and reuse that work.

## The story

A shop stocks items with size codes 0 through 5. One customer asks how many have size below 3;
another asks about size below 5. Rechecking every item for every customer repeats the same work.
A tally by size answers both questions without inspecting each item again.

## The idea in plain language

A **frequency table** records how often each value occurs. A **cumulative count** combines
frequencies across a value boundary. It answers questions about a range of values, not the
positions of those values in the original input.

Two conditions suggest this representation: many queries reuse the same collection, and the
queries care about values or counts rather than the order of occurrences. A small integer
range permits a table indexed directly by value. Huge or unknown ranges require another
representation; allocating one slot for every possible integer is not practical.

## Why Krama needs it

The Day 1 online companion asks a related question for every input position. The central
optimization is to stop repeating work that depends only on the queried value. Equal query
values can reuse the same result. Learning that reasoning prepares you to choose an approach
before you open [the exact assignment](LEETCODE.md).

## The source behind it

[How Many Numbers Are Smaller Than the Current Number](https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/),
`spec:leetcode-1365`, checked 2026-09-22, supplies the companion's strict comparison and bounded
integer domain. The inventory trace and algorithm derivations here are original teaching examples.

## The mechanism

### First derive the direct baseline

Let the inventory be `[3, 1, 3, 0, 5]`. To answer “how many sizes are below 3?”, inspect each
value and count those satisfying `< 3`: 1 and 0, giving 2. For q separate queries, rescanning
n items takes O(nq) time. If q equals n, that becomes O(n²). This is a correct baseline,
and it remains a useful independent check for a faster method on tiny inputs.

### Keep one tally per value

Let U be the number of possible integer values, here 6. Define `frequency[v]` to mean the
number of occurrences of value v. A scan increments the appropriate tally once per item.
The sum of all tallies must be n; that is a useful way to detect lost duplicates.

| Value v | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- | --- |
| frequency[v] | 1 | 1 | 0 | 2 | 0 | 1 |
| Values strictly below v | 0 | 1 | 2 | 2 | 4 | 4 |

For strict comparisons, define `below[v]` as the sum of frequencies with index less than v.
At value v, save the running total **before** adding `frequency[v]`. The total before that
update excludes the current value; the total afterwards includes it. This ordering is the
reason the technique handles ties correctly.

For the table above, before size 3 the running total is 2. Save 2 as `below[3]`, then add the
two size-3 items, making the total 4 for size 4. Query results for sizes 3, 5, and 1 are 2, 4,
and 1. These numbers count occurrences, not distinct size labels.

### Why the reused answer is correct

The frequency scan counts each item in exactly one bucket. Before processing bucket v, the
running total includes exactly buckets 0 through v−1. Saving it answers a strict-lower query;
adding bucket v prepares the invariant for v+1. No bucket is counted twice or omitted.

Grouping loses original positions. If a task wants answers in input order, visit the original
input again and look up each value's answer. Sorting values and returning results in sorted
order would change the output contract.

### Account for the work and the limits

| Approach for q queries | Time | Auxiliary space | When it fits |
| --- | --- | --- | --- |
| Scan per query | O(nq) | O(1), excluding results | Few queries; simple baseline |
| Direct table and cumulative counts | O(n + U + q) | O(U), excluding results | Small bounded integer range |
| Sort a copy and map first positions | O(n log n + q) expected with hash lookups | O(n), excluding results | Queries use observed values; range is large |

For the sorting alternative, all values below x occur before the first x in sorted order.
Its zero-based first position is therefore the number strictly smaller than x. Repeated x
values must share that first position; replacing it with the last position would count ties.
Hash lookup costs in that row are expected, not a universal worst-case guarantee.

That map directly answers only values observed in the input. For an arbitrary absent threshold,
find its insertion boundary in the sorted data instead; an ordered search is a separate operation.
The companion queries its own input values, so every queried value has a recorded first position.

For the online task, the published range has 101 possible values. You can express table work
as O(n + U), and then say why fixed U permits O(n) in that contract. Keep the O(n) required
output separate from the O(U) working storage. A negative value cannot be used as a direct
Python list index for this representation without an intentional offset: it would address
from the end instead of forming a new negative-value bucket.

## When it breaks

The following author demo starts from the inventory's known frequency table. It intentionally
includes size 3 in an answer that should exclude size 3, then fixes the boundary:

```python
frequency = [1, 1, 0, 2, 0, 1]
threshold = 3
wrong = sum(frequency[:threshold + 1])
try:
    assert wrong == 2, "included the threshold bucket in a strict-lower count"
except AssertionError as error:
    print(f"AssertionError: {error}")
correct = sum(frequency[:threshold])
assert correct == 2
print("strict-lower count:", correct)
```

**Line by line:** the table preserves both occurrences of size 3. The slice ending at
`threshold + 1` includes that bucket and produces 4. The assertion catches the boundary
mistake, and the handler prints it. The second slice stops before bucket 3, giving 2.
This slice-based demonstration allocates a temporary list and sums it per query; it illustrates
the boundary only. The cumulative table described above avoids that repeated query work.

Recorded author output on Python 3.12.10, 2026-09-22:

```text
AssertionError: included the threshold bucket in a strict-lower count
strict-lower count: 2
```

## In production

A reused summary is valid only for the collection it summarizes. If stock changes, update or
rebuild the summary before promising current results. A table that is fast but stale answers
a different question. For sparse or extremely large domains, store only observed values and
choose an ordered representation if range queries are needed; an ordinary frequency map alone
does not make strict-lower queries constant-time.

Review question: “Which repeated work disappeared, what memory replaced it, and which input
assumption keeps that memory affordable?” That explanation is more reusable than a code template.

## Check yourself

Before opening the problem, explain these using the table above:

- Why does size 3 have answer 2 even though it appears twice?
- Why must you save the running total before adding the current bucket?
- Why is counting distinct values insufficient?
- What changes if the values include one trillion or negative integers?
- What information must you revisit to return results in original position order?

Then choose your own implementation for [LeetCode practice](LEETCODE.md), justify the baseline,
and compare it with your chosen improvement. A later quick refresher is available in
[DSA recall](../../../docs/DSA_RECALL.md#day-001-counting-and-reusing-counts).
