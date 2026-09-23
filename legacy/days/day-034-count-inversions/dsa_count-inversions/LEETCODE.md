# Day 034 — LeetCode interview practice

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 493. Reverse Pairs

[Open the official problem](https://leetcode.com/problems/reverse-pairs/)

**Difficulty:** Hard. **Original course day:** 34.

**Contract comparison:** Online counts i<j with nums[i]>2*nums[j]; local counts ordinary inversions nums[i]>nums[j]. Use a separate monotone cross-pair counting pass before an ordinary merge for the online route; changing only the merge comparator is incorrect.

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
