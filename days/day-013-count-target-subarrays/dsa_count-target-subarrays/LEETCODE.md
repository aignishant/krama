# Day 013 — LeetCode interview practice

First learn [the mechanism](CONCEPTS.md), trace its example, and check readiness.

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 560. Subarray Sum Equals K

[Open the official problem](https://leetcode.com/problems/subarray-sum-equals-k/)

**Difficulty:** Medium. **Original course day:** 13.

**Contract comparison:** Online and local both count nonempty contiguous intervals with sum k; negative values are allowed. Local solve(data) reads nums and k and returns the integer count.

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
