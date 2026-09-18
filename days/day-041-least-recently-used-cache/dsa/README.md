# Day 041 DSA — Least recently used cache

**Budget:** 60 minutes. **Outcome:** DSA-41. **Theme:** Linked lists and pointer invariants.

## Prerequisite and recall

Prior DSA session: [day 40](../../day-040-remove-from-end/dsa/README.md). Read only its notes if already comfortable.
Recall one candidate, not all of them: [day 40](../../day-040-remove-from-end/dsa/README.md), [day 34](../../day-034-count-inversions/dsa/README.md), [day 20](../../day-020-minimum-positive-window/dsa/README.md)

## Session

| Step | Minutes | Work |
| --- | --- | --- |
| Recall | 5 | Explain a previous invariant without notes. |
| Understand | 10 | Read the contract; trace a small example; choose a baseline. |
| Solve | 30 | Implement the core problem in solution.py without reading hints first. |
| Verify | 10 | Run tests, add boundary cases, explain time and space. |
| Record | 5 | Write the mistake, evidence and next review. |

## Core assignment

**Least recently used cache.** Process [put,key,value] and [get,key] operations with capacity >= 1. Return get results, using -1 for misses. Implement map plus doubly linked nodes.

Start in [PRACTICE.md](PRACTICE.md). The invariant to investigate is kept in
[HINTS.md](HINTS.md), so the first attempt remains independent. Expected target: Expected O(1) per operation; O(capacity) space.
This is a target to justify, not a claim that any implementation meets it.

## Learn and explain

Read [week 6 in the DSA pattern guide](../../../docs/DSA_PATTERN_GUIDE.md) for this week's mechanism before the first attempt.

Before optimizing, write what a straightforward correct algorithm would enumerate or maintain.
On the sample, record the changing state after each meaningful step. Identify what remains true
before and after an update. Explain why termination gives the required answer and whether output
order or mutation is part of the contract. Include Python slicing, sorting and integer costs
when they materially affect your complexity claim.

Reference: [Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/).
Use the lecture notes matching **Linked lists and pointer invariants** for additional teaching; reading the whole
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
