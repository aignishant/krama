# Day 154 DSA — Week 22 DSA review

## Product-company interview practice

Open [today's LeetCode assignment](LEETCODE.md). Use the same 60-minute session;
choose one main attempt rather than adding a second mandatory problem. The local contract
remains the specification for solution.py and cases.json. For an online-only attempt, record
submission evidence, compare the contracts, and use the interview checklist for completion.
The local implementation steps below apply when you choose the local route.

**Budget:** 60 minutes. **Outcome:** DSA-154. **Theme:** Mixed pattern selection II.

## Prerequisite and recall

Prior DSA session: [day 153](../../day-153-minimum-interval-for-queries/dsa_minimum-interval-for-queries/README.md). Read only its notes if already comfortable.
Recall one candidate, not all of them: [day 153](../../day-153-minimum-interval-for-queries/dsa_minimum-interval-for-queries/README.md), [day 147](../../day-147-week-21-review/dsa_week-21-dsa-review/README.md), [day 133](../../day-133-week-19-review/dsa_week-19-dsa-review/README.md)

## Session

| Step | Minutes | Work |
| --- | --- | --- |
| Recall | 5 | Explain a previous invariant without notes. |
| Understand | 10 | Read the contract; trace a small example; choose a baseline. |
| Solve | 30 | Implement the core problem in solution.py without reading hints first. |
| Verify | 10 | Run tests, add boundary cases, explain time and space. |
| Record | 5 | Write the mistake, evidence and next review. |

## Core assignment

**Cold re-solve: Shortest subarray with negatives.** Return shortest nonempty subarray length with sum >= k, or -1; k > 0 and nums may be negative.

Start in [PRACTICE.md](PRACTICE.md). The invariant to investigate is kept in
[HINTS.md](HINTS.md), so the first attempt remains independent. Expected target: O(n) time.
This is a target to justify, not a claim that any implementation meets it.

## Learn and explain

Read [week 22 in the DSA pattern guide](../../../docs/DSA_PATTERN_GUIDE.md) for this week's mechanism before the first attempt.

Before optimizing, write what a straightforward correct algorithm would enumerate or maintain.
On the sample, record the changing state after each meaningful step. Identify what remains true
before and after an update. Explain why termination gives the required answer and whether output
order or mutation is part of the contract. Include Python slicing, sorting and integer costs
when they materially affect your complexity claim.

Reference: [Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/).
Use the lecture notes matching **Mixed pattern selection II** for additional teaching; reading the whole
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
