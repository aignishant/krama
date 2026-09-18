# Day 118 — LeetCode interview practice

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 307. Range Sum Query - Mutable

[Open the official problem](https://leetcode.com/problems/range-sum-query-mutable/)

**Difficulty:** Medium. **Original course day:** 118.

**Contract comparison:** Online range aggregation is SUM, not MIN. Implement its segment-tree variant, then retain the local min exercise to check the changed identity/combine rule.

Official page checked on 2026-09-18; premium statements were not accessible.

## Interview checklist

- [ ] Clarify constraints and explain a baseline before coding.
- [ ] State the invariant or recurrence and why the optimization is valid.
- [ ] Make an independent attempt before hints or an editorial.
- [ ] Test boundary and adversarial cases; record the actual result.
- [ ] Explain time, memory, and one changed-constraint follow-up aloud.
- [ ] Record any hints and a cold re-solve in NOTES.md.

The local `solve(data)` adapter and fixtures do not use the online judge signature.
A local green test is not an online acceptance. Adapt to the official interface when submitting.
