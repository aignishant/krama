# Day 005 — LeetCode interview practice

Before attempting, read [the merge lesson](CONCEPTS.md) and its
[readiness check](CONCEPTS.md#readiness-before-practice). Then read [backward merging](BACKWARD_MERGE.md). [Back to navigation](README.md).

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 88. Merge Sorted Array

[Open the official problem](https://leetcode.com/problems/merge-sorted-array/)

**Difficulty:** Easy. **Original course day:** 5.

**Contract comparison:** Local practice returns a newly allocated list containing all occurrences.
Online, write into `nums1`, which holds `m` valid entries and `n` spare slots; `nums2` holds
`n` entries. Read logical lengths instead of filtering out zero values. Either logical input
may be empty, but their combined length is positive online. The judge observes mutation;
returning a separate merged list does not satisfy that contract.

The [backward-merge lesson](BACKWARD_MERGE.md) derives an O(m+n)-time, O(1)-extra-space route.
The local output itself requires O(m+n) storage.

Official problem statement and constraints rechecked on 2026-09-22; this companion is freely accessible.
Use the current online editor signature. Local tests do not validate that signature or submission.

## Interview checklist

- [ ] Clarify constraints and explain a baseline before coding.
- [ ] State the invariant or recurrence and why the optimization is valid.
- [ ] Make an independent attempt before hints or an editorial.
- [ ] Test boundary and adversarial cases; record the actual result.
- [ ] Explain time, memory, and one changed-constraint follow-up aloud.
- [ ] Record any hints and a cold re-solve in NOTES.md.

The local `solve(data)` adapter and fixtures do not use the online judge signature.
A local green test is not an online acceptance. Adapt to the official interface when submitting.
