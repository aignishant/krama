# Day 036 — LeetCode interview practice

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 206. Reverse Linked List

[Open the official problem](https://leetcode.com/problems/reverse-linked-list/)

**Difficulty:** Easy. **Original course day:** 36.

**Contract comparison:** Online receives a ListNode head and returns the reversed head. Local receives values, requires building real nodes and reversing links, then returns serialized values. Reversing only the input array does not meet the local contract.

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
