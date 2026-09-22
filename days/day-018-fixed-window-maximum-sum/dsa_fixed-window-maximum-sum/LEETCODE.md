# Day 018 — LeetCode interview practice

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 643. Maximum Average Subarray I

[Open the official problem](https://leetcode.com/problems/maximum-average-subarray-i/)

**Difficulty:** Easy. **Original course day:** 18.

**Contract comparison:** Online returns the maximum average of exactly k adjacent values; local practice returns their maximum sum from data["nums"] and data["k"]. Since k is fixed and positive, maximize the sum and divide by k only for the online answer. Both allow negative values and require 1 <= k <= n; the online answer has a floating-point tolerance.

Official public problem page checked on 2026-09-22; see [the source ledger](../../../docs/SOURCES.md).
Learn [the mechanism](CONCEPTS.md) before this attempt; it covers the companion's required variation.

## Interview checklist

- [ ] Clarify constraints and explain a baseline before coding.
- [ ] State the invariant or recurrence and why the optimization is valid.
- [ ] Make an independent attempt before hints or an editorial.
- [ ] Test boundary and adversarial cases; record the actual result.
- [ ] Explain time, memory, and one changed-constraint follow-up aloud.
- [ ] Record any hints and a cold re-solve in NOTES.md.

The local `solve(data)` adapter and fixtures do not use the online judge signature.
A local green test is not an online acceptance. Adapt to the official interface when submitting.
