# Day 026 — LeetCode interview practice

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 1011. Capacity To Ship Packages Within D Days

[Open the official problem](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)

**Difficulty:** Medium. **Original course day:** 26.

**Contract comparison:** Both routes preserve positive parcel weights in order and return minimum capacity within the deadline. Local input is {"weights": [...], "days": ...}; it allows any days>=1, including days greater than the number of parcels. The online constraints bound days by the parcel count. The same feasibility model handles both.

Official problem statement checked on 2026-09-23. Read [the topic explanation](CONCEPTS.md) before practice; adapt to the Python editor signature shown by the online judge.

## Interview checklist

- [ ] Clarify constraints and explain a baseline before coding.
- [ ] State the invariant or recurrence and why the optimization is valid.
- [ ] Make an independent attempt before hints or an editorial.
- [ ] Test boundary and adversarial cases; record the actual result.
- [ ] Explain time, memory, and one changed-constraint follow-up aloud.
- [ ] Record any hints and a cold re-solve in NOTES.md.

The local `solve(data)` adapter and fixtures do not use the online judge signature.
A local green test is not an online acceptance. Adapt to the official interface when submitting.
