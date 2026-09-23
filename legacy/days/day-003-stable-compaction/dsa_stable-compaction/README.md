# Day 003 DSA — Stable compaction

## Navigation — where to start

1. **Learn:** read [the topic explanation](CONCEPTS.md) for the intuition, state, and reasoning.
2. **Trace and check readiness:** follow [the worked example](CONCEPTS.md#worked-trace), then answer [the readiness questions](CONCEPTS.md#readiness-before-practice).
3. **Choose one problem:** open [LeetCode practice](LEETCODE.md) or [the local contract](PRACTICE.md). They are alternative main attempts within the same hour.
4. **Implement independently:** use the online editor for LeetCode, or [solution.py](solution.py) locally. [Hints](HINTS.md) offer help applying the lesson after an attempt.
5. **Verify:** follow [the practice checks](PRACTICE.md#complete-practice-sequence) for the local route, or record an actual online submission result and contract comparison.
6. **Record:** save reasoning, test results, hints, and your next step in [NOTES.md](NOTES.md).
7. **Recall later without practice:** read the [DSA summary file](../../../docs/DSA_RECALL.md#day-003-stable-compaction) for previously studied topics. Cards appear as days are taught; their presence does not mark study complete.

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

## Product-company interview practice

Open [today's LeetCode assignment](LEETCODE.md). Use the same 60-minute session;
choose one main attempt rather than adding a second mandatory problem. The local contract
remains the specification for solution.py and cases.json. For an online-only attempt, record
submission evidence, compare the contracts, and use the interview checklist for completion.
The local implementation steps below apply when you choose the local route.

**Budget:** 60 minutes. **Outcome:** DSA-03. **Theme:** Cost, invariants and arrays.

## Prerequisite and recall

Prior DSA session: [day 2](../../day-002-find-the-first-maximum/dsa_find-the-first-maximum/README.md). Read only its notes if already comfortable.
Recall one candidate, not all of them: [day 2](../../day-002-find-the-first-maximum/dsa_find-the-first-maximum/README.md)

## Session

| Step | Minutes | Work |
| --- | --- | --- |
| Recall | 5 | Explain a previous invariant without notes. |
| Understand | 10 | Read the concept lesson, trace its state, then compare the chosen contract. |
| Solve | 30 | Attempt the online or local problem independently before opening hints. |
| Verify | 10 | Run tests, add boundary cases, explain time and space. |
| Record | 5 | Write the mistake, evidence and next review. |

## Core assignment

**Stable compaction.** Return nums with all zeroes moved to the end, preserving other values' order. Mutate the provided list and return it.

After learning the topic, open [PRACTICE.md](PRACTICE.md). General mechanisms belong in
the explanation; [HINTS.md](HINTS.md) helps apply them after an attempt. Expected target: O(n) time; O(1) auxiliary space.
This is a target to justify, not a claim that any implementation meets it.

## Learn and explain

Start with [CONCEPTS.md](CONCEPTS.md); it teaches the mechanism before the assignment.
The [DSA pattern guide](../../../docs/DSA_PATTERN_GUIDE.md) is optional background.

Before optimizing, write what a straightforward correct algorithm would enumerate or maintain.
On the sample, record the changing state after each meaningful step. Identify what remains true
before and after an update. Explain why termination gives the required answer and whether output
order or mutation is part of the contract. Include Python slicing, sorting and integer costs
when they materially affect your complexity claim.

For the exact online contract and checked official reference, see [LEETCODE.md](LEETCODE.md).
Optional follow-ups use spare time or a later review; they add no mandatory problem.

## Done when

- [ ] Explain the valid prefix, why write never leads read, and why tail cleanup is required.
- [ ] I can restate the contract, including ties, empty input and mutation rules.
- [ ] My chosen route meets its contract: local tests plus self-authored cases, or online submission evidence plus a local-contract comparison.
- [ ] I can justify correctness and the time/space bound.
- [ ] I recorded a wrong approach or counterexample and can explain its repair.
- [ ] I logged complete, partial or needs-review honestly.

If time expires, record the next concrete step in [NOTES.md](NOTES.md). The optional extension
replaces spare time; it is never additional required work.
