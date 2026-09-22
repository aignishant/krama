# Day 133 DSA — Week 19 DSA review

## Navigation — where to start

1. **Cold recall first:** use the assigned review below without notes. Open explanations after the attempt or when deliberately repairing a gap; record any help used.
2. **Repair understanding:** revisit the original subject READMEs linked below, or use the [DSA pattern guide](../../../docs/DSA_PATTERN_GUIDE.md) as a preparation reference.
3. **Choose one problem:** open [LeetCode practice](LEETCODE.md) or [the local contract](PRACTICE.md). They are alternative main attempts within the same hour.
4. **Implement independently:** use the online editor for LeetCode, or [solution.py](solution.py) locally. [Hints](HINTS.md) offer help applying the lesson after an attempt.
5. **Verify:** follow [the practice checks](PRACTICE.md#complete-practice-sequence) for the local route, or record an actual online submission result and contract comparison.
6. **Record:** save reasoning, test results, hints, and your next step in [NOTES.md](NOTES.md).
7. **Recall later without practice:** read the [DSA summary file](../../../docs/DSA_RECALL.md) for previously studied topics. Cards appear as days are taught; their presence does not mark study complete.

Original reading, after cold recall: [Day 127](../../day-127-longest-dag-path/dsa_longest-dag-path/README.md) · [Day 128](../../day-128-minimum-effort-grid-route/dsa_minimum-effort-grid-route/README.md) · [Day 129](../../day-129-redundant-undirected-edge/dsa_redundant-undirected-edge/README.md) · [Day 130](../../day-130-subtree-sizes/dsa_subtree-sizes/README.md) · [Day 131](../../day-131-tree-distance-sums/dsa_tree-distance-sums/README.md) · [Day 132](../../day-132-bipartite-matching/dsa_bipartite-matching/README.md).

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

## Product-company interview practice

Open [today's LeetCode assignment](LEETCODE.md). Use the same 60-minute session;
choose one main attempt rather than adding a second mandatory problem. The local contract
remains the specification for solution.py and cases.json. For an online-only attempt, record
submission evidence, compare the contracts, and use the interview checklist for completion.
The local implementation steps below apply when you choose the local route.

**Budget:** 60 minutes. **Outcome:** DSA-133. **Theme:** Advanced graph and tree practice.

## Prerequisite and recall

Prior DSA session: [day 132](../../day-132-bipartite-matching/dsa_bipartite-matching/README.md). Read only its notes if already comfortable.
Recall one candidate, not all of them: [day 132](../../day-132-bipartite-matching/dsa_bipartite-matching/README.md), [day 126](../../day-126-week-18-review/dsa_week-18-dsa-review/README.md), [day 112](../../day-112-week-16-review/dsa_week-16-dsa-review/README.md)

## Session

| Step | Minutes | Work |
| --- | --- | --- |
| Recall | 5 | Explain a previous invariant without notes. |
| Understand | 10 | Read the contract; trace a small example; choose a baseline. |
| Solve | 30 | Implement the core problem in solution.py without reading hints first. |
| Verify | 10 | Run tests, add boundary cases, explain time and space. |
| Record | 5 | Write the mistake, evidence and next review. |

## Core assignment

**Cold re-solve: Tree distance sums.** Return sum of distances from each vertex to all others in a tree rooted arbitrarily; n >= 1.

After learning the topic, open [PRACTICE.md](PRACTICE.md). General mechanisms belong in
the explanation; [HINTS.md](HINTS.md) helps apply them after an attempt. Expected target: O(n) time; stretch.
This is a target to justify, not a claim that any implementation meets it.

## Learn and explain

Read [week 19 in the DSA pattern guide](../../../docs/DSA_PATTERN_GUIDE.md) for this week's mechanism before the first attempt.

Before optimizing, write what a straightforward correct algorithm would enumerate or maintain.
On the sample, record the changing state after each meaningful step. Identify what remains true
before and after an update. Explain why termination gives the required answer and whether output
order or mutation is part of the contract. Include Python slicing, sorting and integer costs
when they materially affect your complexity claim.

Reference: [Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/).
Use the lecture notes matching **Advanced graph and tree practice** for additional teaching; reading the whole
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
