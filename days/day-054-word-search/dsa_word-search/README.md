# Day 054 DSA — Word search

## Product-company interview practice

Open [today's LeetCode assignment](LEETCODE.md). Use the same 60-minute session;
choose one main attempt rather than adding a second mandatory problem. The local contract
remains the specification for solution.py and cases.json. For an online-only attempt, record
submission evidence, compare the contracts, and use the interview checklist for completion.
The local implementation steps below apply when you choose the local route.

**Budget:** 60 minutes. **Outcome:** DSA-54. **Theme:** Recursion and backtracking.

## Prerequisite and recall

Prior DSA session: [day 53](../../day-053-balanced-parentheses/dsa_balanced-parentheses/README.md). Read only its notes if already comfortable.
Recall one candidate, not all of them: [day 53](../../day-053-balanced-parentheses/dsa_balanced-parentheses/README.md), [day 47](../../day-047-largest-histogram-rectangle/dsa_largest-histogram-rectangle/README.md), [day 33](../../day-033-kth-smallest/dsa_kth-smallest/README.md)

## Session

| Step | Minutes | Work |
| --- | --- | --- |
| Recall | 5 | Explain a previous invariant without notes. |
| Understand | 10 | Read the contract; trace a small example; choose a baseline. |
| Solve | 30 | Implement the core problem in solution.py without reading hints first. |
| Verify | 10 | Run tests, add boundary cases, explain time and space. |
| Record | 5 | Write the mistake, evidence and next review. |

## Core assignment

**Word search.** Return whether word can be formed by orthogonal steps in a rectangular character grid without reusing a cell. Empty word is true.

Start in [PRACTICE.md](PRACTICE.md). The invariant to investigate is kept in
[HINTS.md](HINTS.md), so the first attempt remains independent. Expected target: O(rows*cols*4^L) upper bound.
This is a target to justify, not a claim that any implementation meets it.

## Learn and explain

Read [week 8 in the DSA pattern guide](../../../docs/DSA_PATTERN_GUIDE.md) for this week's mechanism before the first attempt.

Before optimizing, write what a straightforward correct algorithm would enumerate or maintain.
On the sample, record the changing state after each meaningful step. Identify what remains true
before and after an update. Explain why termination gives the required answer and whether output
order or mutation is part of the contract. Include Python slicing, sorting and integer costs
when they materially affect your complexity claim.

Reference: [Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/).
Use the lecture notes matching **Recursion and backtracking** for additional teaching; reading the whole
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
