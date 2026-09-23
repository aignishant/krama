# Day 026 DSA — Minimum shipping capacity

## Navigation — where to start

1. **Learn the topic:** read [CONCEPTS.md](CONCEPTS.md) for intuition, the mechanism, its proof or tradeoff, and its limits.
2. **Trace and check readiness:** follow [the worked trace](CONCEPTS.md#worked-trace), then answer [the readiness questions](CONCEPTS.md#readiness-before-practice).
3. **Choose one problem:** open [LeetCode practice](LEETCODE.md) or [the local contract](PRACTICE.md). They are alternative main attempts within the same hour.
4. **Implement independently:** use the online editor for LeetCode, or [solution.py](solution.py) locally. [Hints](HINTS.md) offer help applying the lesson after an attempt.
5. **Verify:** follow [the practice checks](PRACTICE.md#complete-practice-sequence) for the local route, or record an actual online submission result and contract comparison.
6. **Record:** save reasoning, test results, hints, and your next step in [NOTES.md](NOTES.md).
7. **Recall later without practice:** read the [DSA summary file](../../../docs/DSA_RECALL.md) for previously studied topics. Cards appear as days are taught; their presence does not mark study complete.

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

## Product-company interview practice

Open [today's LeetCode assignment](LEETCODE.md). Use the same 60-minute session;
choose one main attempt rather than adding a second mandatory problem. The local contract
remains the specification for solution.py and cases.json. For an online-only attempt, record
submission evidence, compare the contracts, and use the interview checklist for completion.
The local implementation steps below apply when you choose the local route.

**Budget:** 60 minutes. **Outcome:** DSA-26. **Theme:** Binary search and ordered answers.

## Prerequisite and recall

Prior DSA session: [day 25](../../day-025-integer-square-root/dsa_integer-square-root/README.md). Read only its notes if already comfortable.
Recall one candidate, not all of them: [day 25](../../day-025-integer-square-root/dsa_integer-square-root/README.md), [day 19](../../day-019-longest-distinct-substring/dsa_longest-distinct-substring/README.md), [day 5](../../day-005-merge-sorted-arrays/dsa_merge-sorted-arrays/README.md)

## Session

| Step | Minutes | Work |
| --- | --- | --- |
| Recall | 5 | Explain a previous invariant without notes. |
| Understand | 10 | Read the contract; trace a small example; choose a baseline. |
| Solve | 30 | Implement the core problem in solution.py without reading hints first. |
| Verify | 10 | Run tests, add boundary cases, explain time and space. |
| Record | 5 | Write the mistake, evidence and next review. |

## Core assignment

**Minimum shipping capacity.** Return smallest daily capacity shipping positive weights in given order within days; weights nonempty and days >= 1.

After learning the topic, open [PRACTICE.md](PRACTICE.md). General mechanisms belong in
the explanation; [HINTS.md](HINTS.md) helps apply them after an attempt. Expected target: O(n log sum(weights)) time.
This is a target to justify, not a claim that any implementation meets it.

## Learn and explain

Read [CONCEPTS.md](CONCEPTS.md) before the first attempt; trace the mechanism and check readiness.

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
