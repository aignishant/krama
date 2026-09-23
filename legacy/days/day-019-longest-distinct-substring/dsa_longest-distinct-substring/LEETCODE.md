# Day 019 — LeetCode interview practice

Use this inside the existing **60-minute DSA budget**. Choose the online problem or
the local exercise as the main attempt; use its companion as a variation or review.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 3. Longest Substring Without Repeating Characters

[Open the official problem](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

**Difficulty:** Medium. **Original course day:** 19.

**Contract comparison:** Both return a length, not the substring. Local input uses data["text"] and explicitly treats Python string elements as Unicode code points, without normalization; the online page describes English letters, digits, symbols, and spaces. Empty input returns 0. A substring is contiguous, unlike a subsequence.

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
