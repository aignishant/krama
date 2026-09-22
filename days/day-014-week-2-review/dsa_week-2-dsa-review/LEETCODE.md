# Day 014 — LeetCode interview practice

Begin cold; read [the review explanation](CONCEPTS.md) after the attempts or record help used.

Use this inside the existing **60-minute DSA budget**. Complete two cold re-solves, choosing the online or
local version of each assigned problem. Do not double the quota across platforms.

[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)

## 217. Contains Duplicate

[Open the official problem](https://leetcode.com/problems/contains-duplicate/)

**Difficulty:** Easy. **Original course day:** 8.

**Contract comparison:** Online returns a boolean for any duplicate; local practice returns the first value whose second occurrence is encountered.

Official public statement checked on 2026-09-22.

## 303. Range Sum Query - Immutable

[Open the official problem](https://leetcode.com/problems/range-sum-query-immutable/)

**Difficulty:** Easy. **Original course day:** 12.

**Contract comparison:** Online constructs NumArray once and calls sumRange(left, right) for inclusive queries; local solve(data) returns a list for a query batch and allows empty nums only with no queries.

Official public statement checked on 2026-09-22.

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
A harder unresolved problem may replace the second re-solve; keep two attempts. No new problem quota.
