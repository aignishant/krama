# Day 035 — LeetCode interview practice

Use this inside the existing **60-minute DSA budget**. Choose the online or
local routes for the two scheduled re-solves. Open repair reading afterwards.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 912. Sort an Array

[Open the official problem](https://leetcode.com/problems/sort-an-array/)

**Difficulty:** Medium. **Original course day:** 29.

**Contract comparison:** Online sorts numbers; local practice sorts records and explicitly checks stability.

Official statement checked on 2026-09-23; this companion is publicly readable.

## 215. Kth Largest Element in an Array

[Open the official problem](https://leetcode.com/problems/kth-largest-element-in-an-array/)

**Difficulty:** Medium. **Original course day:** 33.

**Contract comparison:** Online target is n-k in ascending order; local target is k-1. Both count duplicate values as separate ranks.

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

## Review pacing

5 minutes recall, 20 minutes per cold attempt, 10 minutes critique and 5 minutes logging.
A harder unresolved problem may replace the second attempt slot. No new problem quota.

[Teaching route](CONCEPTS.md) — repair reading after cold attempts.
