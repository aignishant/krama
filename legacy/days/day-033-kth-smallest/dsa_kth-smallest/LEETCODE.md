# Day 033 — LeetCode interview practice

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 215. Kth Largest Element in an Array

[Open the official problem](https://leetcode.com/problems/kth-largest-element-in-an-array/)

**Difficulty:** Medium. **Original course day:** 33.

**Contract comparison:** Online selects kth LARGEST (ascending zero-based target n-k); local selects kth SMALLEST (target k-1). Both count duplicates as separate ranks; local requires partition-based selection.

Official statement checked on 2026-09-23; this companion is publicly readable.

## Interview checklist

- [ ] Clarify constraints and explain a baseline before coding.
- [ ] State the invariant or recurrence and why the optimization is valid.
- [ ] Make an independent attempt before hints or an editorial.
- [ ] Test boundary and adversarial cases; record the actual result.
- [ ] Explain time, memory, and one changed-constraint follow-up aloud.
- [ ] Record any hints and a cold re-solve in NOTES.md.

The local `solve(data)` adapter and fixtures do not use the online judge signature.
A local green test is not an online acceptance. Adapt to the official interface when submitting.

[Teaching route](CONCEPTS.md) — includes the mechanism needed for the chosen contract.
