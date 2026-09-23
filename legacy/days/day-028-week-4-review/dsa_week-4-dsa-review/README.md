# Day 028 DSA — Week 4 DSA review

## Navigation — where to start

1. **Cold recall first:** use the assigned review below without notes. Open explanations after the attempt or when deliberately repairing a gap; record any help used.
2. **Repair after the cold attempt:** open [the review lesson](CONCEPTS.md), its [worked trace](CONCEPTS.md#worked-trace), and [readiness checks](CONCEPTS.md#readiness-before-practice). Record any help used.
3. **Use the weekly assessment:** follow [the two cold re-solves](PRACTICE.md#weekly-assessment), using [LeetCode](LEETCODE.md) or the local route within the same hour.
4. **Implement independently:** use the online editor for LeetCode, or [solution.py](solution.py) locally. [Hints](HINTS.md) offer help applying the lesson after an attempt.
5. **Verify:** follow [the practice checks](PRACTICE.md#complete-practice-sequence) for the local route, or record an actual online submission result and contract comparison.
6. **Record:** save reasoning, test results, hints, and your next step in [NOTES.md](NOTES.md).
7. **Recall later without practice:** read the [DSA summary file](../../../docs/DSA_RECALL.md) for previously studied topics. Cards appear as days are taught; their presence does not mark study complete.

Original reading, after cold recall: [Day 22](../../day-022-lower-bound/dsa_lower-bound/README.md) · [Day 23](../../day-023-target-range/dsa_target-range/README.md) · [Day 24](../../day-024-rotated-search/dsa_rotated-search/README.md) · [Day 25](../../day-025-integer-square-root/dsa_integer-square-root/README.md) · [Day 26](../../day-026-minimum-shipping-capacity/dsa_minimum-shipping-capacity/README.md) · [Day 27](../../day-027-median-of-two-arrays/dsa_median-of-two-arrays/README.md).

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

## Product-company interview practice

Open [today's LeetCode assignment](LEETCODE.md). Use the same 60-minute session;
use the two scheduled cold re-solves rather than adding a new problem quota. The local contract
remains the specification for solution.py and cases.json. For an online-only attempt, record
submission evidence, compare the contracts, and use the interview checklist for completion.
The local implementation steps below apply when you choose the local route.

**Budget:** 60 minutes. **Outcome:** DSA-28. **Theme:** Binary search and ordered answers.

## Prerequisite and recall

Prior DSA session: [day 27](../../day-027-median-of-two-arrays/dsa_median-of-two-arrays/README.md). Read only its notes if already comfortable.
Recall one candidate, not all of them: [day 27](../../day-027-median-of-two-arrays/dsa_median-of-two-arrays/README.md), [day 21](../../day-021-week-3-review/dsa_week-3-dsa-review/README.md), [day 7](../../day-007-week-1-review/dsa_week-1-dsa-review/README.md)

## Session

Use 5 minutes recall, 20 minutes for each of two cold re-solves, 10 minutes critique, and 5 minutes logging. Follow [the weekly assessment](PRACTICE.md#weekly-assessment); repair reading comes afterwards.

## Core assignment

**Cold re-solve: Minimum shipping capacity.** Return smallest daily capacity shipping positive weights in given order within days; weights nonempty and days >= 1.

For the cold assessment, open [PRACTICE.md](PRACTICE.md). General mechanisms belong in
the explanation; [HINTS.md](HINTS.md) helps apply them after an attempt. Expected target: O(n log sum(weights)) time.
This is a target to justify, not a claim that any implementation meets it.

## Learn and explain

After the cold attempts, use [CONCEPTS.md](CONCEPTS.md) to repair the mechanism and explain your counterexample.

Before optimizing, write what a straightforward correct algorithm would enumerate or maintain.
On the sample, record the changing state after each meaningful step. Identify what remains true
before and after an update. Explain why termination gives the required answer and whether output
order or mutation is part of the contract. Include Python slicing, sorting and integer costs
when they materially affect your complexity claim.

Reference: [Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/).
Use the lecture notes matching **Binary search and ordered answers** for additional teaching; reading the whole
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
