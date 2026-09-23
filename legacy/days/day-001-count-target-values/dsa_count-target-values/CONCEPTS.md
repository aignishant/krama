---
day: 1
part: "1.1"
title: "Give each step of a scan a precise meaning"
ids: [DSA-01]
level: foundation
prerequisites: ["Python loops and functions"]
failure: true
---

# Give each step of a scan a precise meaning

Start here before opening a problem. Read the counting explanation, trace the example, and
answer the readiness questions. For the local route this is the core lesson. For the LeetCode
route, continue to [Reuse counts across many questions](FREQUENCY_COUNTS.md) before attempting
the companion. That extra reading replaces part of this session's concept time or continues
in another sitting; it does not add a second mandatory problem.

## One-line answer

A scan is easier to prove correct when its saved state describes exactly the items already processed.

## The story

You check a shopping receipt, adding one price at a time. Halfway down the receipt, your running
total is useful, but it is not the final bill. If you stop after the first line, your arithmetic
can be correct while your answer is wrong. The missing piece is knowing which lines the total covers.

## The idea in plain language

A **contract** says what inputs are allowed, what result is required, and what side effects are
permitted. For the local exercise, the result is one count and the input list must remain unchanged.
The LeetCode companion has a different contract: its result contains one answer per position.
Learn the mechanism first; compare the exact problem contracts when you reach practice.

A **loop invariant** is a statement that stays true at a specified point in every iteration.
It connects the saved state to the work completed. “The variable is correct” is too vague;
“before the next iteration, this total is the sum of the first k prices” can be checked.

A **baseline** is a straightforward correct approach against which another approach can be
compared. It need not be inefficient. Some tasks are already optimally handled by a simple scan.

## Why Krama needs it

In [Day 2's maximum scan](../../day-002-find-the-first-maximum/dsa_find-the-first-maximum/README.md),
you will need to explain which positions a saved candidate represents. The same proof structure
later helps with windows and search boundaries. Today's goal is to learn that structure before
the state becomes complicated.

## The mechanism

### Recognize a counting problem

Ask what makes a single item contribute to the answer. A **predicate** is a condition with a
yes/no result: a receipt item is discounted, a request succeeded, or a value equals a target.
If each item contributes independently and you need only how many qualify, a running count
is sufficient. You do not need to save the qualifying items or their positions.

That is the useful insight behind a scan: discard details that cannot change the requested
answer. A sum retains the total contribution; a count retains the number of successful checks.
For counting, interpret a yes as 1 and a no as 0. This converts a verbal question into adding
small contributions. Sorting does not help a single independent predicate check.

This recognition rule has limits. “Find the first match” needs a position; “find adjacent
matches” needs a relationship between items; “return the matching items” needs output storage.
Do not apply a count-only representation when the contract needs information it discards.

### Trace a count before writing code

Teaching example: count discounted entries on a receipt, in the order
`[regular, discounted, discounted, regular, discounted]`.

| Items processed | Current label | Contribution | Count afterwards |
| --- | --- | --- | --- |
| 0 | None yet | None | 0 |
| 1 | regular | 0 | 0 |
| 2 | discounted | 1 | 1 |
| 3 | discounted | 1 | 2 |
| 4 | regular | 0 | 2 |
| 5 | discounted | 1 | 3 |

The saved count means “number of qualifying entries among the items already processed.”
Initialize it to zero, inspect each entry once, increase it only when the predicate succeeds,
and return it after the scan ends. Duplicates are separate occurrences; a set would lose them.

Why does this work? Initially no entries have been processed, so the count is zero. Each next
entry either adds one qualifying occurrence or adds none. Both updates preserve the meaning.
When no entries remain, the processed portion is the whole receipt. Empty input needs no
special update: the initial count is already the answer. A non-match must not reset the count;
it says nothing about matches found earlier.

### Connect counting to a general accumulator

Use this **sum demonstration**, then transfer the reasoning to your own counting solution.
This example is teaching code; it is not the implementation of `solve(data)`.

```python
values = [4, -1, 2]
total = 0
for processed, value in enumerate(values, start=1):
    total += value
    print(f"processed={processed}, total={total}")
assert total == 5
print("sum check: PASS")
```

**Line by line:** `values` supplies a positive, a negative, and another positive contribution.
`total = 0` represents the sum before any item is processed. `enumerate(..., start=1)` labels
the number of processed items after this iteration's update; it is not a zero-based index.
`+=` incorporates exactly the current contribution. The print records the state after the update.
The assertion checks the final result against an independently calculated answer.

Observed with Python 3.12.10 during author verification on 2026-09-19:

```text
processed=1, total=4
processed=2, total=3
processed=3, total=5
sum check: PASS
```

| Point | Processed values | Meaning of total |
| --- | --- | --- |
| Before the loop | none | Empty sum, 0 |
| After iteration 1 | 4 | Sum of first 1 value, 4 |
| After iteration 2 | 4, -1 | Sum of first 2 values, 3 |
| After iteration 3 | 4, -1, 2 | Sum of all 3 values, 5 |

The proof has three obligations:

1. **Initialization:** zero describes the empty prefix.
2. **Maintenance:** adding the next value extends the prefix by exactly one item.
3. **Termination:** once every item is processed, the prefix is the entire input.

For your counting exercise, write your own state meaning and explain what happens on both a
match and a non-match. Keep the point of the invariant consistent: before an update or after it.

**Cost:** with n values, this demonstration performs n updates. Ignoring diagnostic printing
and using the course's unit-cost number model, its running time is O(n). The saved state uses
O(1) auxiliary space: a fixed number of variables, excluding the supplied input. It returns no
collection. This is an asymptotic argument, not a measured speed claim.

Two consecutive scans still take O(n) time because n + n = 2n. Comparing every element with
every element performs n² comparisons. A temporary list of n matches uses O(n) auxiliary space
even if the final returned count is only one integer. Read the operations inside a loop before
deciding its cost.

## When it breaks

This deliberately broken sum returns a valid prefix total too early:

```python
def broken_total(values):
    total = 0
    for value in values:
        total += value
        return total
    return total

try:
    assert broken_total([4, -1, 2]) == 5, "returned before all items were processed"
except AssertionError as error:
    print(f"AssertionError: {error}")
```

**Line by line:** the accumulator update is valid, but the indented `return` exits during the
first iteration. The final return handles only an empty input in this broken version. The
assertion detects the incorrect result; the exception handler prints the failure so this
teaching snippet can continue normally. An uncaught assertion in a test should fail the test run.

Actual printed failure from the author run:

```text
AssertionError: returned before all items were processed
```

Move the return outside the loop, then rerun. A one-element example cannot expose this bug;
two nonzero contributions can. An invariant holding so far does not justify returning before
the termination condition needed by the proof.

## In production

For one query over a collection, prefer a clear scan or a suitable built-in after establishing
its contract. Repeated queries over the same data may justify building a frequency table once;
that trades memory and maintenance work for cheaper later queries. Do not build it automatically
for a single target.

At scale, input copies and repeated scans can dominate work. A function that silently sorts
its caller's list may break unrelated code even when its own numeric result is right. A useful
review comment is: “Show that the input stays unchanged and explain all temporary allocations.”

Interview follow-up: if a supposedly exact algorithm skips one position in an arbitrary,
unsorted input, could changing only that unseen value change the answer? Use that reasoning
to explain why a worst-case linear scan is necessary for a single exact target-count query
without a precomputed index.

## Check yourself

### Readiness before practice

Answer from the explanation before opening the assignment:

1. Why does `[discounted, regular, discounted]` finish at 2 rather than 1?
2. Why can you discard the positions of qualifying entries in a count-only task?
3. What would force you to retain more information than one counter?
4. Why is returning at the first match valid for existence but invalid for total occurrences?
5. Why does one full scan use O(n) time even when very few entries qualify?

You are ready when you can describe the predicate, state meaning, both update cases, and
termination without copying code. If those are unclear, reread the trace. For the online route,
read [the frequency and cumulative-count lesson](FREQUENCY_COUNTS.md) next.

### Practice after the explanation

Run the two teaching snippets in a scratch Python session. Repair the early-return example and
verify both a multi-element input and an empty input. Then close the demonstration and implement
your chosen assignment independently.

For the local route, run `python course.py practice 1` from the repository root after editing
[solution.py](solution.py). The existing starter raises `NotImplementedError`; that is intentional.
Add your own distinguishing cases to [cases.json](cases.json): empty, singleton, repeated matches,
no matches, and a match at the last position are useful categories. Pick at least four new cases
and calculate their answers before running them. Also verify input preservation; output checks
alone do not establish it.

Say out loud: “What does my state mean, why does each update preserve that meaning, and why is
the state sufficient when the loop ends?” Record your argument and actual test output in
[NOTES.md](NOTES.md). The online route instead needs actual submission evidence and its own
complexity explanation; local O(n) expectations do not automatically apply to that problem.

**Optional follow-ups:** consider repeated target queries or streaming values. State the changed
contract first, then explain what state you would retain. Use spare time or a later review.

**Next:** [Local practice](PRACTICE.md), or learn [reused counts](FREQUENCY_COUNTS.md) before
[LeetCode practice](LEETCODE.md). For a later refresher, use [DSA recall](../../../docs/DSA_RECALL.md#day-001-counting-and-reusing-counts).
