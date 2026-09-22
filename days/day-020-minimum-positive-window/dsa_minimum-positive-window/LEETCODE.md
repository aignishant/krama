# Day 020 — LeetCode interview practice

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 209. Minimum Size Subarray Sum

[Open the official problem](https://leetcode.com/problems/minimum-size-subarray-sum/)

**Difficulty:** Medium. **Original course day:** 20.

**Contract comparison:** Both ask for the shortest nonempty contiguous subarray with sum >= target, returning 0 if none qualifies. Values and target are positive integers. Local input uses data["nums"] and data["target"]; empty local input has no answer, while online constraints require at least one element. Negative values invalidate the positive-window proof. The online O(n log n) follow-up is optional.

Official public problem page checked on 2026-09-22; see [the source ledger](../../../docs/SOURCES.md).
Learn [the mechanism](CONCEPTS.md) before this attempt; it covers the companion's required variation.

## Interview checklist

- [ ] Clarify constraints and explain a baseline before coding.
- [ ] State the invariant or recurrence and why the optimization is valid.
- [ ] Make an independent attempt before hints or an editorial.
- [ ] Test boundary and adversarial cases; record the actual result.
- [ ] Explain time, memory, and one changed-constraint follow-up aloud.
- [ ] Record any hints and a cold re-solve in NOTES.md.

The local `solve(data)` adapter and fixtures do not use the online judge signature.
A local green test is not an online acceptance. Adapt to the official interface when submitting.
