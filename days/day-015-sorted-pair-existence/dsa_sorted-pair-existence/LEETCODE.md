# Day 015 — LeetCode interview practice

First learn [the mechanism](CONCEPTS.md), trace its example, and check readiness.

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 167. Two Sum II - Input Array Is Sorted

[Open the official problem](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)

**Difficulty:** Medium. **Original course day:** 15.

**Contract comparison:** Online returns the two one-based indices, promises exactly one solution, and requires constant extra space. Local returns a boolean, including False for no pair, and permits multiple possible pairs.

Official public statement checked on 2026-09-22.

## Interview checklist

- [ ] Clarify constraints and explain a baseline before coding.
- [ ] State the invariant or recurrence and why the optimization is valid.
- [ ] Make an independent attempt before hints or an editorial.
- [ ] Test boundary and adversarial cases; record the actual result.
- [ ] Explain time, memory, and one changed-constraint follow-up aloud.
- [ ] Record any hints and a cold re-solve in NOTES.md.

The local `solve(data)` adapter and fixtures do not use the online judge signature.
A local green test is not an online acceptance. Adapt to the official interface when submitting.
