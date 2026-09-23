# Day 002 — LeetCode interview practice

Before attempting, read [the concept lesson](CONCEPTS.md) and its
[readiness check](CONCEPTS.md#readiness-before-practice). Then read [dominance checks](DOMINANCE.md). [Back to navigation](README.md).

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 747. Largest Number At Least Twice of Others

[Open the official problem](https://leetcode.com/problems/largest-number-at-least-twice-of-others/)

**Difficulty:** Easy. **Original course day:** 2.

**Contract comparison:** The local task accepts empty input and ties and returns the earliest maximum index. Online, the array has at least two nonnegative integers and a unique maximum; return its index only if it meets the dominance condition, otherwise -1. Read [the dominance lesson](DOMINANCE.md) before attempting it.

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
