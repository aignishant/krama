# Day 001 — LeetCode interview practice

## Before opening the problem

Read [counting and invariants](CONCEPTS.md), then [reusing counts across queries](FREQUENCY_COUNTS.md).
The second lesson explains the direct baseline, frequency tables, strict cumulative counts,
duplicates, output ordering, and when sorting is an alternative. Answer its readiness points
before attempting this problem. [README navigation](README.md) shows the full route.

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 1365. How Many Numbers Are Smaller Than the Current Number

[Open the official problem](https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/)

**Difficulty:** Easy. **Original course day:** 1.

**Contract comparison:** Related counting drill: the online problem counts smaller values for each position, not occurrences of one target.

Official public problem description opened again on 2026-09-19: problem number, Easy
difficulty, strict comparison, and constraints verified. This is source verification, not
an accepted submission.

## Understand the two contracts

| Detail | Local exercise | LeetCode 1365 |
| --- | --- | --- |
| Inputs | `nums` and one `target` in `data` | `nums` |
| Result | One integer | One integer per input position, in corresponding order |
| Predicate | Equal to the target | Strictly less than the value at this position |
| Duplicates | Each matching occurrence contributes | Equal values do not count as smaller; repeated smaller values each contribute |
| Bounds | Integer values; empty input allowed; no fixed size/value bounds | 2 to 500 elements; integer values from 0 to 100 |
| Interface | `solve(data)` returns a JSON-compatible result | Use the Python interface supplied by the online judge |
| Verification | Local fixtures plus your own cases and input-preservation check | Actual online submission result plus your own explanation and tests |

The local contract forbids mutation. The online description does not supply that same explicit
restriction; explain any copying or mutation choice and preserve the association with original
positions. Do not assume local adapter code can be pasted directly into the online judge.

For an original hand trace, use `[5, 2, 2, 9]`. The result is `[2, 0, 0, 3]`: the two 2s each
contribute when examining 5, while neither 2 is smaller than the other. This differs from asking
how often one target occurs. Empty-input tests belong to an extended/local contract; they are
outside the published online bounds.

## Your attempt

After [the two teaching parts](README.md), explain a direct baseline before optimizing.
For each output position, describe what must be examined and counted. Derive the total work
from that description; do not reuse the local O(n) target without justification. Distinguish
auxiliary space from the required O(n) output.

Use duplicate values, all-equal values, minimum valid length, and boundary values to challenge
your idea. First calculate expected answers independently. Use the bounded-range reasoning from
the frequency lesson to choose an improvement and explain why it is valid. General techniques
are taught before practice; your implementation and application of them are the independent work.

Keep the attempt within the same hour. If you use the online route, record the problem number,
language, actual verdict, submission reference if available, complexity, hints used, and one
contract difference in [NOTES.md](NOTES.md). Leave the local starter unsolved unless you choose
it as a separate variation or later review.

## Interview checklist

- [ ] Clarify constraints and explain a baseline before coding.
- [ ] State the invariant or recurrence and why the optimization is valid.
- [ ] Make an independent attempt before hints or an editorial.
- [ ] Test boundary and adversarial cases; record the actual result.
- [ ] Explain time, memory, and one changed-constraint follow-up aloud.
- [ ] Record any hints and a cold re-solve in NOTES.md.

The local `solve(data)` adapter and fixtures do not use the online judge signature.
A local green test is not an online acceptance. Adapt to the official interface when submitting.
