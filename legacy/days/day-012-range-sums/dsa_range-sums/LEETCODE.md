# Day 012 — LeetCode interview practice

Start with [the concepts](CONCEPTS.md), [worked trace](CONCEPTS.md#worked-trace), and
[readiness check](CONCEPTS.md#readiness-before-practice). General techniques are taught there;
choose one main practice route within the existing 60-minute budget.


Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 303. Range Sum Query - Immutable

[Open the official problem](https://leetcode.com/problems/range-sum-query-immutable/)

**Difficulty:** Easy. **Original course day:** 12.

**Contract comparison:** Online uses NumArray(nums) followed by sumRange(left, right) calls on nonempty input. Local solve(data) returns all inclusive query answers in query order, and permits empty nums only with no queries. Precompute once in the online constructor; local tests do not test the class interface.

Official problem statement checked live on 2026-09-22. No online submission is claimed.

## Interview checklist

- [ ] Clarify constraints and explain a baseline before coding.
- [ ] State the invariant or recurrence and why the optimization is valid.
- [ ] Make an independent attempt before hints or an editorial.
- [ ] Test boundary and adversarial cases; record the actual result.
- [ ] Explain time, memory, and one changed-constraint follow-up aloud.
- [ ] Record any hints and a cold re-solve in NOTES.md.

The local `solve(data)` adapter and fixtures do not use the online judge signature.
A local green test is not an online acceptance. Adapt to the official interface when submitting.
