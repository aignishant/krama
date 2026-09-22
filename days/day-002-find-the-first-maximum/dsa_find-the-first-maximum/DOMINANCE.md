---
day: 2
part: "1.2"
title: "Separate finding a candidate from verifying its dominance"
ids: [DSA-02]
level: working
prerequisites: ["First-maximum scan"]
failure: true
---

# Separate finding a candidate from verifying its dominance

Read after [the maximum lesson](CONCEPTS.md). This supplies the additional idea required by
the online route; it is optional depth for the local route, within the same DSA budget.

## One-line answer

Being the largest establishes a candidate; a dominance requirement still needs its own proof.

## The story

One bid is highest, but the sale rule requires it to be at least twice every competing bid.
A bid of 11 beats 7 without doubling it. Announcing the winner after the maximum scan applies
only half the rule.

## The idea in plain language

A universal condition means the candidate must pass a comparison against **each other** item.
One failed comparison is enough to reject it. Finding the candidate and validating it in two
passes is often clearer than forcing every requirement into one pass.

## Why Krama needs it

The local exercise returns the first maximum even when it barely beats another value. The
online companion can reject its largest value. Reusing a pattern does not make contracts equal.

## The source behind it

The official [Largest Number At Least Twice of Others](https://leetcode.com/problems/largest-number-at-least-twice-of-others/)
page, checked 2026-09-22, specifies nonnegative integers, at least two items, and a unique
maximum. The online rejection result is −1. See `spec:leetcode-747` in
[the source ledger](../../../docs/SOURCES.md). The derivation below is an original teaching example.

## The mechanism

### Worked trace

For bids `[2, 12, 5, 1]`, the maximum candidate is at index 1.

| Competing index | Competing bid | Twice the bid | Does 12 cover it? |
| --- | --- | --- | --- |
| 0 | 2 | 4 | Yes |
| 2 | 5 | 10 | Yes |
| 3 | 1 | 2 | Yes |

Skip the candidate **by index**: “every other” excludes that position. During verification,
all competitors already examined satisfy the condition. A failure settles rejection; finishing
without failure establishes the universal claim. Two scans take O(n)+O(n)=O(n) time and O(1)
auxiliary space, with no mutation needed.

Optional optimization: retain the two largest values from distinct positions. On a new largest
value, the old largest becomes second-largest. Otherwise compare against the second-largest.
Checking the largest against twice the second-largest suffices because doubling preserves
order. The second-largest bounds every competitor. Initialize from actual items or an explicit
missing state; don't accidentally use the largest twice. This saves a pass, not an asymptotic
factor, and introduces more state to prove correct.

## When it breaks

```python
bids = [2, 12, 5, 1]
candidate = max(bids)
wrong = all(candidate >= 2 * bid for bid in bids)
print("including self:", wrong)
try:
    assert wrong, "the winning bid was compared against itself"
except AssertionError as error:
    print(f"AssertionError: {error}")
competitors = [2, 5, 1]
assert all(candidate >= 2 * bid for bid in competitors)
print("competitors only: PASS")
```

**Line by line:** `max` supplies this teaching fixture's candidate. `all` requires each comparison
to pass, but the first version includes 12 against 24. The assertion exposes that false rejection.
The explicitly listed competitors isolate the intended condition. This small fixture allocates
a list for clarity; your constant-space verification should skip the candidate in the original input.

Author verification on Python 3.12.10, 2026-09-22:

```text
including self: False
AssertionError: the winning bid was compared against itself
competitors only: PASS
```

Checking only one convenient competitor is also wrong: `[1, 11, 7]` passes against 1 but fails
against 7. Equality at the threshold must pass: “at least” is inclusive.

## In production

Separate candidate selection from eligibility checks in ranking pipelines. A highest-scoring
record may still fail a business constraint. A second linear pass can improve reviewability
when the data is already in memory; a stream may justify the two-largest summary instead.

## Check yourself

### Readiness before practice

Explain why `[1, 10, 5]` passes and `[1, 10, 6]` fails. State why skipping the candidate is
necessary and why the second-largest is sufficient. Contrast online assumptions with the
local empty-input and duplicate-maximum cases before opening [LeetCode practice](LEETCODE.md).
Record actual submission evidence in [NOTES.md](NOTES.md); author checks are not acceptance.

[Back to the main lesson](CONCEPTS.md) · [Navigation](README.md)
