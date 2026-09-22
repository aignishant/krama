# Day 006 DSA — Best single trade

## Navigation — where to start

1. **Learn:** read [CONCEPTS.md](CONCEPTS.md) for the mechanism, reasoning, costs, and limits.
2. **Trace and check readiness:** follow the [worked trace](CONCEPTS.md#worked-trace), inspect the observed failure, and answer the [readiness questions](CONCEPTS.md#readiness-before-practice).
3. **Read the exact contracts:** Open [LeetCode practice](LEETCODE.md) or [the local contract](PRACTICE.md); choose one main attempt within the same hour.
4. **Implement independently:** use the online editor or [solution.py](solution.py) for the local target. Use [hints](HINTS.md) only after an attempt.
5. **Verify:** follow [the practice checks](PRACTICE.md#complete-practice-sequence), or record online submission evidence and the local-contract comparison.
6. **Record:** save actual results, reasoning, help used, and next steps in [NOTES.md](NOTES.md).
7. **Recall later without practice:** use the [track recall cards](../../../docs/DSA_RECALL.md) for topics already studied; cards do not mark completion.

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

## Product-company interview practice

Open [today's LeetCode assignment](LEETCODE.md). Use the same 60-minute session;
choose one main attempt rather than adding a second mandatory problem. The local contract
remains the specification for solution.py and cases.json. For an online-only attempt, record
submission evidence, compare the contracts, and use the interview checklist for completion.
The local implementation steps below apply when you choose the local route.

**Budget:** 60 minutes. **Outcome:** DSA-06. **Theme:** Cost, invariants and arrays.

## Prerequisite and recall

Prior DSA session: [day 5](../../day-005-merge-sorted-arrays/dsa_merge-sorted-arrays/README.md). Read only its notes if already comfortable.
Recall one candidate, not all of them: [day 5](../../day-005-merge-sorted-arrays/dsa_merge-sorted-arrays/README.md)

## Session

| Step | Minutes | Work |
| --- | --- | --- |
| Recall | 5 | Explain a previous invariant without notes. |
| Understand | 10 | Read the contract; trace a small example; choose a baseline. |
| Solve | 30 | Implement the core problem in solution.py without reading hints first. |
| Verify | 10 | Run tests, add boundary cases, explain time and space. |
| Record | 5 | Write the mistake, evidence and next review. |

## Core assignment

**Best single trade.** Given daily prices, return the largest nonnegative profit from one buy followed by one sell; no trade returns 0.

After learning the topic, open [PRACTICE.md](PRACTICE.md). General mechanisms belong in
the explanation; [HINTS.md](HINTS.md) helps apply them after an attempt. Expected target: O(n) time; O(1) space.
This is a target to justify, not a claim that any implementation meets it.

## Learn and explain

Read [the topic explanation](CONCEPTS.md) and its readiness check before the first attempt.

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

- [ ] I can restate the contract, including ties, empty input and mutation rules.
- [ ] My chosen route meets its contract: local tests plus self-authored cases, or online submission evidence plus a local-contract comparison.
- [ ] I can justify correctness and the time/space bound.
- [ ] I recorded a wrong approach or counterexample and can explain its repair.
- [ ] I logged complete, partial or needs-review honestly.

If time expires, record the next concrete step in [NOTES.md](NOTES.md). The optional extension
replaces spare time; it is never additional required work.
