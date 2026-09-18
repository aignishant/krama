# Day 089 DSA — Task cooldown length

**Budget:** 60 minutes. **Outcome:** DSA-89. **Theme:** Greedy choices and exchange arguments.

## Prerequisite and recall

Prior DSA session: [day 88](../../day-088-circular-fuel-route/dsa/README.md). Read only its notes if already comfortable.
Recall one candidate, not all of them: [day 88](../../day-088-circular-fuel-route/dsa/README.md), [day 82](../../day-082-strong-components/dsa/README.md), [day 68](../../day-068-tree-reconstruction/dsa/README.md)

## Session

| Step | Minutes | Work |
| --- | --- | --- |
| Recall | 5 | Explain a previous invariant without notes. |
| Understand | 10 | Read the contract; trace a small example; choose a baseline. |
| Solve | 30 | Implement the core problem in solution.py without reading hints first. |
| Verify | 10 | Run tests, add boundary cases, explain time and space. |
| Record | 5 | Write the mistake, evidence and next review. |

## Core assignment

**Task cooldown length.** Uppercase tasks take one slot, same task occurrences need at least n intervening slots. Return minimum total slots including idle.

Start in [PRACTICE.md](PRACTICE.md). The invariant to investigate is kept in
[HINTS.md](HINTS.md), so the first attempt remains independent. Expected target: O(number of tasks + alphabet size).
This is a target to justify, not a claim that any implementation meets it.

## Learn and explain

Read [week 13 in the DSA pattern guide](../../../docs/DSA_PATTERN_GUIDE.md) for this week's mechanism before the first attempt.

Before optimizing, write what a straightforward correct algorithm would enumerate or maintain.
On the sample, record the changing state after each meaningful step. Identify what remains true
before and after an update. Explain why termination gives the required answer and whether output
order or mutation is part of the contract. Include Python slicing, sorting and integer costs
when they materially affect your complexity claim.

Reference: [Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/).
Use the lecture notes matching **Greedy choices and exchange arguments** for additional teaching; reading the whole
course is not assigned. Advanced topics beyond that reference are introduced by their practice
contracts and staged hints; use a review session for deeper derivations.

## Done when

- [ ] I can restate the contract, including ties, empty input and mutation rules.
- [ ] The core solution passes provided and self-authored tests.
- [ ] I can justify correctness and the time/space bound.
- [ ] I recorded a wrong approach or counterexample and can explain its repair.
- [ ] I logged complete, partial or needs-review honestly.

If time expires, record the next concrete step in [NOTES.md](NOTES.md). The optional extension
replaces spare time; it is never additional required work.
