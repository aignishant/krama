# Day 009 — LeetCode interview practice

Start with [the concepts](CONCEPTS.md), [worked trace](CONCEPTS.md#worked-trace), and
[readiness check](CONCEPTS.md#readiness-before-practice). General techniques are taught there;
choose one main practice route within the existing 60-minute budget.


Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 347. Top K Frequent Elements

[Open the official problem](https://leetcode.com/problems/top-k-frequent-elements/)

**Difficulty:** Medium. **Original course day:** 9.

**Contract comparison:** Online returns k values, permits arbitrary result order, and guarantees a unique answer. Local ranks all distinct integers, breaking frequency ties by ascending value. Learn frequency buckets for the online better-than-O(n log n) follow-up; sorting all distinct values alone does not meet it in general.

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
