# Day 017 — LeetCode interview practice

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 11. Container With Most Water

[Open the official problem](https://leetcode.com/problems/container-with-most-water/)

**Difficulty:** Medium. **Original course day:** 17.

**Contract comparison:** Both return the maximum area, not wall indices. Online input has at least two nonnegative heights; local input uses data["heights"] and returns 0 for fewer than two. Preserve original positions: sorting heights changes the problem.

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
