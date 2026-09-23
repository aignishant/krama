# Day 014 DSA — Week 2 DSA review

## Navigation — where to start

1. **Cold recall first:** use the assigned review below without notes. Open explanations after the attempt or when deliberately repairing a gap; record any help used.
2. **Repair after the cold attempt:** read [the review explanation](CONCEPTS.md), [worked trace](CONCEPTS.md#worked-trace), and [readiness questions](CONCEPTS.md#readiness-before-practice).
3. **Choose the review route:** open [LeetCode practice](LEETCODE.md) or [the local contract](PRACTICE.md). Each route covers two cold re-solves within the same hour.
4. **Implement independently:** use the online editor for LeetCode, or [solution.py](solution.py) locally. [Hints](HINTS.md) offer help applying the lesson after an attempt.
5. **Verify:** follow [the practice checks](PRACTICE.md#complete-practice-sequence) for the local route, or record an actual online submission result and contract comparison.
6. **Record:** save reasoning, test results, hints, and your next step in [NOTES.md](NOTES.md).
7. **Recall later without practice:** read [this day's card](../../../docs/DSA_RECALL.md#day-014-week-2-dsa-review) for a previously studied topic; reading is not completion.

Original reading, after cold recall: [Day 8](../../day-008-first-repeated-value/dsa_first-repeated-value/README.md) · [Day 9](../../day-009-frequency-ranking/dsa_frequency-ranking/README.md) · [Day 10](../../day-010-pair-sum-indices/dsa_pair-sum-indices/README.md) · [Day 11](../../day-011-group-anagrams/dsa_group-anagrams/README.md) · [Day 12](../../day-012-range-sums/dsa_range-sums/README.md) · [Day 13](../../day-013-count-target-subarrays/dsa_count-target-subarrays/README.md).

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

## Product-company interview practice

Open [today's LeetCode assignment](LEETCODE.md). Use the same 60-minute session;
complete the two scheduled cold re-solves, choosing local or online format for each. The local contract
remains the specification for solution.py and cases.json. For an online-only attempt, record
submission evidence, compare the contracts, and use the interview checklist for completion.
The local implementation steps below apply when you choose the local route.

**Budget:** 60 minutes. **Outcome:** DSA-14. **Theme:** Hashing and prefix sums.

## Prerequisite and recall

Prior DSA session: [day 13](../../day-013-count-target-subarrays/dsa_count-target-subarrays/README.md). Keep its notes closed until after the cold attempts.
Recall one candidate, not all of them: [day 13](../../day-013-count-target-subarrays/dsa_count-target-subarrays/README.md), [day 7](../../day-007-week-1-review/dsa_week-1-dsa-review/README.md)

## Session

Use 5 minutes cold recall, 20 minutes for each of two cold re-solves, 10 minutes critique,
and 5 minutes logging. Choose local or online format for each assigned review problem;
the two solves remain required, without doubling them across platforms. Use
[the weekly assessment](PRACTICE.md#weekly-assessment) for targets and scoring.
Read explanations and hints only after the cold attempts, or record help used.

## Core assignment

**Cold re-solve: Range sums.** For each inclusive [left,right] query return the sum. Queries are valid for nums; an empty nums has no queries.

For the cold assignment, open [PRACTICE.md](PRACTICE.md). General mechanisms belong in
the explanation; [HINTS.md](HINTS.md) helps apply them after an attempt. Expected target: O(n+q) time; O(n) space.
This is a target to justify, not a claim that any implementation meets it.

## Learn and explain

After both cold attempts, use [the review explanation](CONCEPTS.md) to repair the specific gap.

Before optimizing, write what a straightforward correct algorithm would enumerate or maintain.
On the sample, record the changing state after each meaningful step. Identify what remains true
before and after an update. Explain why termination gives the required answer and whether output
order or mutation is part of the contract. Include Python slicing, sorting and integer costs
when they materially affect your complexity claim.

Reference: [Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/).
Use the lecture notes matching **Hashing and prefix sums** for additional teaching; reading the whole
course is not assigned. Advanced topics beyond that reference are introduced by their practice
contracts and staged hints; use a review session for deeper derivations.

## Done when

- [ ] I can restate the contract, including ties, empty input and mutation rules.
- [ ] My chosen route meets its contract: local tests plus self-authored cases, or online submission evidence plus a local-contract comparison.
- [ ] I can justify correctness and the time/space bound.
- [ ] I recorded a wrong approach or counterexample and can explain its repair.
- [ ] I logged complete, partial or needs-review honestly.

If time expires, record the next concrete step in [NOTES.md](NOTES.md). The optional extension
replaces spare time; it is never additional required work.
