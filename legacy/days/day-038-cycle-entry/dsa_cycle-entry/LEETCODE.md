# Day 038 — LeetCode interview practice

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 142. Linked List Cycle II

[Open the official problem](https://leetcode.com/problems/linked-list-cycle-ii/)

**Difficulty:** Medium. **Original course day:** 38.

**Contract comparison:** Online receives only head, returns the entry node or None, and forbids link mutation. Its pos is judge construction metadata, not a function argument. Local uses values/pos to build the topology, detects from head, and returns the zero-based entry index or -1. Do not return pos without performing detection.

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
