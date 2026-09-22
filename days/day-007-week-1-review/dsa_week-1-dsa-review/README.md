# Day 007 DSA — Week 1 DSA review

## Navigation — where to start

1. **Choose the contracts:** use the [local pair](PRACTICE.md#weekly-assessment) or [online pair](LEETCODE.md) within one hour.
2. **Attempt cold:** re-solve both from blank code without notes, old solutions, hints, or references. The local [solution.py](solution.py) is for the second solve; keep the first in separate scratch code.
3. **Verify:** test each attempt against its own contract, explain its invariant and costs, and apply [the review rubric](PRACTICE.md#weekly-assessment).
4. **Repair afterwards:** read [CONCEPTS.md](CONCEPTS.md), its [worked trace](CONCEPTS.md#worked-trace), and [readiness questions](CONCEPTS.md#readiness-after-repair). Use the original lessons below for specific gaps.
5. **Recheck:** test the repaired behavior and explain it aloud. Record any [hints](HINTS.md) used; a repaired attempt does not retroactively become hint-free.
6. **Record:** save both attempts, scores, actual results, help used, and next steps in [NOTES.md](NOTES.md).
7. **Recall later without practice:** use [DSA recall](../../../docs/DSA_RECALL.md) for studied topics; it does not pass the cold assessment.

Original reading, after cold recall: [Day 1](../../day-001-count-target-values/dsa_count-target-values/README.md) · [Day 2](../../day-002-find-the-first-maximum/dsa_find-the-first-maximum/README.md) · [Day 3](../../day-003-stable-compaction/dsa_stable-compaction/README.md) · [Day 4](../../day-004-reverse-a-segment/dsa_reverse-a-segment/README.md) · [Day 5](../../day-005-merge-sorted-arrays/dsa_merge-sorted-arrays/README.md) · [Day 6](../../day-006-best-single-trade/dsa_best-single-trade/README.md).

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

## Product-company interview practice

Use [the online pair](LEETCODE.md) or [the local pair](PRACTICE.md#weekly-assessment)
for the two cold re-solves in this 60-minute review. The local review fixture checks only
the second solve, merge; verify the first solve against its own contract and fixtures.
Online attempts require actual submission evidence and contract comparisons.

**Budget:** 60 minutes. **Outcome:** DSA-07. **Theme:** Cost, invariants and arrays.

## Prerequisite and recall

Prior DSA session: [day 6](../../day-006-best-single-trade/dsa_best-single-trade/README.md).
Recall from memory before opening prior notes. Use the original lessons above only for repair.

## Session

| Step | Minutes | Work |
| --- | --- | --- |
| Recall | 5 | Restate the two contracts without opening old solutions. |
| First re-solve | 20 | Re-solve Day 1's local or online counting task from blank code. |
| Second re-solve | 20 | Re-solve Day 5's matching merge task; an unresolved problem may replace this slot. |
| Critique | 10 | Test both attempts, explain invariants and costs, then repair gaps. |
| Record | 5 | Score both attempts, record help, and schedule the next cold review. |

## Core assignment

**Cold re-solve: Merge sorted arrays.** Return a new sorted list containing all values from sorted lists a and b, including duplicates.

Open [PRACTICE.md](PRACTICE.md) for both cold tasks before reading explanations.
This folder's starter implements only the second task. Keep the first attempt in separate
scratch code so prior learner work is preserved. Expected merge target: O(n+m) time; output space O(n+m).
This is a target to justify, not a claim that any implementation meets it.

## Learn and explain

After the cold attempts, use [CONCEPTS.md](CONCEPTS.md) and its original-lesson links to repair
specific gaps. Do not read a pattern guide or hints before an attempt you intend to score as cold.

Before optimizing, write what a straightforward correct algorithm would enumerate or maintain.
On the sample, record the changing state after each meaningful step. Identify what remains true
before and after an update. Explain why termination gives the required answer and whether output
order or mutation is part of the contract. Include Python slicing, sorting and integer costs
when they materially affect your complexity claim.

Reference: [Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/).
Use the lecture notes matching **Cost, invariants and arrays** for additional teaching; reading the whole
course is not assigned. Advanced topics beyond that reference are introduced by their practice
contracts and staged hints; use a review session for deeper derivations.

## Done when

- [ ] I completed two cold re-solves and scored each at least 6/8 across correctness, explanation, complexity, and tests, with correctness=2 and at least one hint-free solve.
- [ ] I can restate the contract, including ties, empty input and mutation rules.
- [ ] My chosen route meets its contract: local tests plus self-authored cases, or online submission evidence plus a local-contract comparison.
- [ ] I can justify correctness and the time/space bound.
- [ ] I recorded a wrong approach or counterexample and can explain its repair.
- [ ] I logged complete, partial or needs-review honestly.

If time expires, record the next concrete step in [NOTES.md](NOTES.md). The optional extension
replaces spare time; it is never additional required work.
