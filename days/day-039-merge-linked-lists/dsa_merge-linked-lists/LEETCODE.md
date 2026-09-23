# Day 039 — LeetCode interview practice

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 21. Merge Two Sorted Lists

[Open the official problem](https://leetcode.com/problems/merge-two-sorted-lists/)

**Difficulty:** Easy. **Original course day:** 39.

**Contract comparison:** Online receives list1/list2 heads and returns a merged head by splicing original nodes. Local builds from a/b, relinks original nodes, and returns serialized values. Both inputs are sorted; the construction yields disjoint chains. Choosing the left input on ties is a documented deterministic convention, not an extra online requirement.

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
