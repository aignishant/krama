# Day 005 DSA — Merge sorted arrays

## Navigation — where to start

1. **Learn:** read [the topic explanation](CONCEPTS.md) for the intuition, mechanism, and limits. The online route also needs [backward merging](BACKWARD_MERGE.md); optional for the local route.
2. **Trace and check readiness:** follow [the worked trace](CONCEPTS.md#worked-trace), then answer [the readiness questions](CONCEPTS.md#readiness-before-practice).
3. **Choose one problem:** open [LeetCode practice](LEETCODE.md) or [the local contract](PRACTICE.md). They are alternative main attempts within the same hour.
4. **Implement independently:** use the online editor for LeetCode, or [solution.py](solution.py) locally. [Hints](HINTS.md) offer help applying the lesson after an attempt.
5. **Verify:** follow [the practice checks](PRACTICE.md#complete-practice-sequence) for the local route, or record an actual online submission result and contract comparison.
6. **Record:** save reasoning, test results, hints, and your next step in [NOTES.md](NOTES.md).
7. **Recall later without practice:** read the [DSA summary file](../../../docs/DSA_RECALL.md#day-005-merge-sorted-arrays) for previously studied topics. Cards appear as days are taught; their presence does not mark study complete.

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

## Product-company interview practice

Open [today's LeetCode assignment](LEETCODE.md). Use the same 60-minute session;
choose one main attempt rather than adding a second mandatory problem. The local contract
remains the specification for solution.py and cases.json. For an online-only attempt, record
submission evidence, compare the contracts, and use the interview checklist for completion.
The local implementation steps below apply when you choose the local route.

**Budget:** 60 minutes. **Outcome:** DSA-05. **Theme:** Cost, invariants and arrays.

## Prerequisite and recall

Prior DSA session: [day 4](../../day-004-reverse-a-segment/dsa_reverse-a-segment/README.md). Read only its notes if already comfortable.
Recall one candidate, not all of them: [day 4](../../day-004-reverse-a-segment/dsa_reverse-a-segment/README.md)

## Session

| Step | Minutes | Work |
| --- | --- | --- |
| Recall | 5 | Explain a previous invariant without notes. |
| Understand | 10 | Read the lesson, trace the state, then compare the chosen contract. |
| Solve | 30 | Attempt the online or local route independently before opening hints. |
| Verify | 10 | Run tests, add boundary cases, explain time and space. |
| Record | 5 | Write the mistake, evidence and next review. |

## Core assignment

**Merge sorted arrays.** Return a new sorted list containing all values from sorted lists a and b, including duplicates.

After learning the topic, open [PRACTICE.md](PRACTICE.md). General mechanisms belong in
the explanation; [HINTS.md](HINTS.md) helps apply them after an attempt. Expected target: O(n+m) time; output space O(n+m).
This is a target to justify, not a claim that any implementation meets it.

## Learn and explain

Start with [CONCEPTS.md](CONCEPTS.md): compare the unconsumed heads, preserve all occurrences,
and finish the remaining tail. Explain why sorted inputs justify the choice and separate
required output space from auxiliary memory. For the online destination-buffer contract,
continue to [BACKWARD_MERGE.md](BACKWARD_MERGE.md) and explain why writing from the right is safe.

The [pattern guide](../../../docs/DSA_PATTERN_GUIDE.md) is optional background. Exact online
constraints and the checked official reference are in [LEETCODE.md](LEETCODE.md).

## Done when

- [ ] Explain why only the two heads need comparison, preserve duplicates, and account for tail cleanup and output memory.
- [ ] I can restate the contract, including ties, empty input and mutation rules.
- [ ] My chosen route meets its contract: local tests plus self-authored cases, or online submission evidence plus a local-contract comparison.
- [ ] I can justify correctness and the time/space bound.
- [ ] I recorded a wrong approach or counterexample and can explain its repair.
- [ ] I logged complete, partial or needs-review honestly.

If time expires, record the next concrete step in [NOTES.md](NOTES.md). The optional extension
replaces spare time; it is never additional required work.
