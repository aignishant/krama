# Day 003 — LeetCode interview practice

Before attempting, read [the concept lesson](CONCEPTS.md) and its
[readiness check](CONCEPTS.md#readiness-before-practice). [Back to navigation](README.md).

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 283. Move Zeroes

[Open the official problem](https://leetcode.com/problems/move-zeroes/)

**Difficulty:** Easy. **Original course day:** 3.

**Contract comparison:** Both routes preserve nonzero order and mutate the original list. The local adapter also returns that same list; the online judge observes the mutated argument. Online input is nonempty. Include negative nonzero values when checking either route.

Official problem statement and constraints rechecked on 2026-09-22; this companion is freely accessible.
Use the online editor's current signature; local tests validate only the local adapter.

## Interview checklist

- [ ] Clarify constraints and explain a baseline before coding.
- [ ] State the invariant or recurrence and why the optimization is valid.
- [ ] Make an independent attempt before hints or an editorial.
- [ ] Test boundary and adversarial cases; record the actual result.
- [ ] Explain time, memory, and one changed-constraint follow-up aloud.
- [ ] Record any hints and a cold re-solve in NOTES.md.

The local `solve(data)` adapter and fixtures do not use the online judge signature.
A local green test is not an online acceptance. Adapt to the official interface when submitting.
