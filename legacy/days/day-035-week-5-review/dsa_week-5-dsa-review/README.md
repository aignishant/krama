# Day 035 DSA — Week 5 DSA review

## Navigation — where to start

1. **Cold recall first:** use the assigned review below without notes. Open explanations after the attempt or when deliberately repairing a gap; record any help used.
2. **Repair after the cold attempt:** read [the review lesson](CONCEPTS.md), its [worked trace](CONCEPTS.md#worked-trace), and [readiness checks](CONCEPTS.md#readiness-before-practice). Record help used.
3. **Attempt two cold re-solves:** use [the review contract](PRACTICE.md#weekly-assessment) or [the online companions](LEETCODE.md) for Day 29 and Day 33. A harder unresolved problem may replace the second slot.
4. **Implement independently:** use the online editor for LeetCode, or [solution.py](solution.py) locally. [Hints](HINTS.md) offer help applying the lesson after an attempt.
5. **Verify:** follow [the practice checks](PRACTICE.md#complete-practice-sequence) for the local route, or record an actual online submission result and contract comparison.
6. **Record:** save reasoning, test results, hints, and your next step in [NOTES.md](NOTES.md).
7. **Recall later without practice:** read the [DSA summary file](../../../docs/DSA_RECALL.md) for previously studied topics. Cards appear as days are taught; their presence does not mark study complete.

Original reading, after cold recall: [Day 29](../../day-029-stable-record-sorting/dsa_stable-record-sorting/README.md) · [Day 30](../../day-030-merge-overlapping-intervals/dsa_merge-overlapping-intervals/README.md) · [Day 31](../../day-031-insert-an-interval/dsa_insert-an-interval/README.md) · [Day 32](../../day-032-minimum-meeting-rooms/dsa_minimum-meeting-rooms/README.md) · [Day 33](../../day-033-kth-smallest/dsa_kth-smallest/README.md) · [Day 34](../../day-034-count-inversions/dsa_count-inversions/README.md).

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

## Product-company interview practice

Open [today's LeetCode assignment](LEETCODE.md). Use the same 60-minute session;
use the two scheduled cold re-solves below; do not add a new problem quota. The local contract
remains the specification for solution.py and cases.json. For an online-only attempt, record
submission evidence, compare the contracts, and use the interview checklist for completion.
The local implementation steps below apply when you choose the local route.

**Budget:** 60 minutes. **Outcome:** DSA-35. **Theme:** Sorting, intervals and selection.

## Prerequisite and recall

Prior DSA session: [day 34](../../day-034-count-inversions/dsa_count-inversions/README.md). Read only its notes if already comfortable.
Recall one candidate, not all of them: [day 34](../../day-034-count-inversions/dsa_count-inversions/README.md), [day 28](../../day-028-week-4-review/dsa_week-4-dsa-review/README.md), [day 14](../../day-014-week-2-review/dsa_week-2-dsa-review/README.md)

## Session

| Step | Minutes | Work |
| --- | --- | --- |
| Recall | 5 | Recall the mechanisms without notes. |
| First re-solve | 20 | Day 29 stable sorting from blank code. |
| Second re-solve | 20 | Day 33 selection, or one harder unresolved problem. |
| Critique | 10 | Test both attempts, explain invariants and costs, then repair. |
| Record | 5 | Score evidence and log help and remaining gaps. |

## Core assignment

**Cold re-solve: Kth smallest.** Return kth smallest value, counting duplicates; k is one-based and valid. Implement partition-based selection.

Start cold with [PRACTICE.md](PRACTICE.md); open explanations afterwards. General mechanisms belong in
the explanation; [HINTS.md](HINTS.md) helps apply them after an attempt. Expected target: Expected O(n), worst O(n^2); explain pivot choice.
This is a target to justify, not a claim that any implementation meets it.

## Learn and explain

Read [the topic lesson](CONCEPTS.md) after the cold attempts for repair.

Before optimizing, write what a straightforward correct algorithm would enumerate or maintain.
On the sample, record the changing state after each meaningful step. Identify what remains true
before and after an update. Explain why termination gives the required answer and whether output
order or mutation is part of the contract. Include Python slicing, sorting and integer costs
when they materially affect your complexity claim.

Reference: [Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/).
Use the lecture notes matching **Sorting, intervals and selection** for additional teaching; reading the whole
course is not assigned. Advanced topics beyond that reference are introduced by their practice
contracts and staged hints; use a review session for deeper derivations.

## Done when

- [ ] I attempted both scheduled cold re-solves and verified them separately; the Day 35 fixture checks only selection.
- [ ] I scored correctness/explanation/complexity/tests 0–2 each, reaching 6/8 with correctness=2 and at least one hint-free solve, or recorded partial/needs-review.
- [ ] I can restate the contract, including ties, empty input and mutation rules.
- [ ] My chosen route meets its contract: local tests plus self-authored cases, or online submission evidence plus a local-contract comparison.
- [ ] I can justify correctness and the time/space bound.
- [ ] I recorded a wrong approach or counterexample and can explain its repair.
- [ ] I logged complete, partial or needs-review honestly.

If time expires, record the next concrete step in [NOTES.md](NOTES.md). The optional extension
replaces spare time; it is never additional required work.
