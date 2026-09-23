---
day: 8
part: "1.1"
title: "Remember the distinct values already encountered"
ids: [DSA-08]
level: working
prerequisites: ["Prefix invariants", "Equality"]
failure: true
---

# Remember the distinct values already encountered

Core: understand membership, trace the first repeated encounter, and compare the Boolean
online contract. Custom hash behavior and unbounded streams are optional depth.

## One-line answer

Check whether the current value is already in the processed prefix before adding it to the remembered set.

## The story

At a parcel counter, you record each ticket number as it arrives. The first number presented
twice is the first repeated encounter, even if another ticket number appeared earlier in the queue.

## The idea in plain language

The local task returns the value whose second occurrence has the smallest index. It does not
ask for the smallest repeated value or the repeated value with the earliest first occurrence.
For `[7, 2, 2, 7]`, the answer is 2 because its second occurrence arrives first.

A set records distinct values and supports a membership question: has an equal value been
seen? It discards counts and order, which are unnecessary here because the scan itself supplies
encounter order. A direct baseline checks each current value against every earlier value,
costing O(n²) time in the no-duplicate case and O(1) auxiliary space with index loops.
Remembered membership avoids those repeated prefix scans under the usual hash-table model.

Recognize the pattern when you need exact “seen before” information. A running minimum cannot
answer membership; retaining all prior distinct values preserves the information the query needs.

## Why Krama needs it

[Frequency ranking](../../day-009-frequency-ranking/dsa_frequency-ranking/README.md) will need
counts rather than presence, and [pair sum](../../day-010-pair-sum-indices/dsa_pair-sum-indices/README.md)
will ask about a complementary value. Learn which information to save before changing containers.

## The source behind it

[Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) (`spec:leetcode-217`)
asks a Boolean existence question. [Built-in Types](https://docs.python.org/3.12/library/stdtypes.html#set-types-set-frozenset)
(`spec:python-3.12-builtins`) defines Python sets and membership. Both were checked 2026-09-22.
The original trace uses integers so membership has an explicit, ordinary equality model.

## The mechanism

### Worked trace

| Index | Ticket | Set before checking | Already present? | Action |
| --- | --- | --- | --- | --- |
| 0 | 7 | {} | No | Remember 7 |
| 1 | 2 | {7} | No | Remember 2 |
| 2 | 2 | {7, 2} | Yes | Stop with 2 |
| 3 | 7 | Not reached | — | No later event can be first |

Before processing index i, the set contains exactly the distinct values at indices below i.
It starts empty. If the current value is absent, adding it maintains the statement for the
next index. If it is present, some earlier index has the same value. Since the algorithm would
have stopped at any earlier repeat, this is the earliest second encounter. Exhausting the
input without that event means no duplicate exists.

Check before insertion. Inserting first makes every value appear previously seen, including
the first element. Empty local input returns `None`; repeated zero returns `0`, which must
not be tested for existence with truthiness. The online contract returns `True` or `False`
instead and requires a nonempty input. A set-size comparison can answer the online Boolean
question but loses the local first-encounter answer and normally consumes the whole input.

For n fixed-size integers, expected hash lookup/insertion cost gives expected O(n) time and
O(k) auxiliary space for k remembered distinct values, O(n) in the worst case. Output is O(1).
This is not a universal worst-case constant-time lookup guarantee: collisions can produce
quadratic total work. Large integers or custom equality/hash methods add their own cost.
Sorting is an alternative for Boolean detection at O(n log n) comparisons, but changes order
and cannot directly answer the local encounter-order question.

## When it breaks

```python
tickets = [7, 2, 2, 7]
wrong = next(value for value in tickets if tickets.count(value) > 1)
seen = set()
trace = []
answer = None
for value in tickets:
    repeated = value in seen
    trace.append((value, repeated))
    if repeated:
        answer = value
        break
    seen.add(value)
print("first-occurrence shortcut:", wrong)
print("encounter trace:", trace, "answer:", answer)
try:
    assert wrong == answer, "earliest first occurrence is the wrong order"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert answer == 2
print("encounter-order check: PASS")
```

**Line by line:** `count` looks at the entire input, so the shortcut chooses 7 before its
second occurrence happens. The teaching scan records membership before insertion. Stopping on
the first true membership event preserves the contract. The deliberate assertion distinguishes
the two orderings. `trace` is teaching instrumentation and adds O(n) space; it is not needed
by an implementation. The `count` shortcut can also take O(n²) time.

Author verification on Python 3.12.10, 2026-09-22:

```text
first-occurrence shortcut: 7
encounter trace: [(7, False), (2, False), (2, True)] answer: 2
AssertionError: earliest first occurrence is the wrong order
encounter-order check: PASS
```

## In production

Define the supported value domain before using a set: lists are unhashable, and `False`, `0`,
and `0.0` compare equal in ordinary Python membership. Mixed-type application identifiers may
need validation or a different key policy. See [hash and equality](../../day-004-reverse-a-segment/lang_hash-and-equality/CONCEPTS.md)
for the obligation that equal keys have equal hashes.

An unbounded stream of distinct values requires growing memory for this exact approach.
Eviction changes the question to repetition within retained history; approximate filters may
introduce false positives. A reviewer should ask whether a memory cap changes the product
promise, and whether tests distinguish duplicate existence from which repeat occurs first.

## Check yourself

### Readiness before practice

1. What is the answer for `[5, 1, 1, 5]`, and which index makes it final?
2. Why must membership be tested before insertion?
3. How do you distinguish repeated zero from no repeated value?
4. What does the set forget, and why is that safe for this task?

Run the trace, then use [PRACTICE.md](PRACTICE.md) or [LEETCODE.md](LEETCODE.md) for your own
attempt. Explain correctness aloud and test no answer, an immediate repeat, repeated zero,
and competing repeated values. Keep one main route within 60 minutes and save [NOTES.md](NOTES.md).

[Navigation](README.md) · [Quick recall](../../../docs/DSA_RECALL.md#day-008-first-repeated-value)
