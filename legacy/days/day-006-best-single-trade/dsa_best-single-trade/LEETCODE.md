# Day 006 — LeetCode interview practice

**Learn first:** read [CONCEPTS.md](CONCEPTS.md), trace the mechanism, and check readiness
before choosing this practice route.

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 121. Best Time to Buy and Sell Stock

[Open the official problem](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)

**Difficulty:** Easy. **Original course day:** 6.

**Contract comparison:** Both return the largest nonnegative profit from one purchase followed
by a later sale, with zero for no profitable trade. Locally use `solve({"prices": [...]})`;
the online method receives the prices list directly. The online input is nonempty; the local
lesson also covers an empty list, which has no eligible pair and returns zero. Neither needs
input mutation or a choice of trade indices.

Official problem page rechecked on 2026-09-22; this assignment's statement was accessible.

## Interview checklist

- [ ] Clarify constraints and explain a baseline before coding.
- [ ] State the invariant or recurrence and why the optimization is valid.
- [ ] Make an independent attempt before hints or an editorial.
- [ ] Test boundary and adversarial cases; record the actual result.
- [ ] Explain time, memory, and one changed-constraint follow-up aloud.
- [ ] Record any hints and a cold re-solve in NOTES.md.

The local `solve(data)` adapter and fixtures do not use the online judge signature.
A local green test is not an online acceptance. Adapt to the official interface when submitting.
