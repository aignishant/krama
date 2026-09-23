# Day 040 — LeetCode interview practice

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 19. Remove Nth Node From End of List

[Open the official problem](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)

**Difficulty:** Medium. **Original course day:** 40.

**Contract comparison:** Online receives head and a valid n, removes that node counted from the end, and returns the new head. Local builds from values and returns serialized remaining values. Both assume 1 <= n <= length, so an empty input or invalid n is outside this assignment. A singleton removal returns None online and [] locally.

Official public problem statement checked on 2026-09-23. Learn [the pointer mechanism](CONCEPTS.md) before attempting; no additional algorithm is required for this companion.

## Interview checklist

- [ ] Clarify constraints and explain a baseline before coding.
- [ ] State the invariant or recurrence and why the optimization is valid.
- [ ] Make an independent attempt before hints or an editorial.
- [ ] Test boundary and adversarial cases; record the actual result.
- [ ] Explain time, memory, and one changed-constraint follow-up aloud.
- [ ] Record any hints and a cold re-solve in NOTES.md.

The local `solve(data)` adapter and fixtures do not use the online judge signature.
A local green test is not an online acceptance. Adapt to the official interface when submitting.
