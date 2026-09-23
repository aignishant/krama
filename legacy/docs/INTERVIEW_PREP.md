# DSA for product-company interviews

The goal is to solve an unfamiliar problem and defend the result, including in preparation for
Google and similar product companies. The assignments are recommendations for broad interview
skills; they are not verified company-tagged questions or a prediction of a specific interview.

## One hour, one main attempt

| Minutes | Activity |
| --- | --- |
| 0–5 | Cold recall of a prior invariant or mistake. |
| 5–15 | Read the statement, clarify constraints, trace an example and explain a baseline. |
| 15–45 | Independently solve the assigned LeetCode problem or its local fallback. |
| 45–55 | Test edge cases, explain the proof and analyze time and auxiliary/output space. |
| 55–60 | Record submission evidence, hints, mistakes and the next review. |

Use the local problem as a warm-up or variation when useful. Do not complete two separate full
solutions just to tick two boxes. If the LeetCode companion is only loosely related, the daily
LEETCODE.md identifies the difference; keep the local problem for the exact course objective.
Premium companions are optional: their local equivalents keep the course usable without payment.
Hard problems may span review sessions. A meaningful incomplete attempt is recorded as partial.

## Explain these before and after coding

- Input/output contract: valid bounds, duplicates, ordering, mutation, missing answers and ties.
- Baseline: why it works and exactly where it wastes time or memory.
- Improved mechanism: the invariant, recurrence or exchange argument that makes it correct.
- Complexity: include preprocessing, output size and Python copying/sorting costs.
- Tests: normal, minimal, repeated/equal, impossible and adversarial cases when permitted.
- Follow-up: what changes for streaming input, less memory, repeated queries or different constraints?

Practice saying the reasoning aloud. Readable names and a small defensible implementation are
more useful than unexplained memorized templates. If you use a hint, record it and re-solve cold.

## Progression

Weeks 1–5 establish arrays, hashing, windows, search and sorting. Weeks 6–13 add lists, trees,
heaps, graphs and greedy proofs. Weeks 14–20 develop DP, strings and data structure design.
Weeks 21–22 mix patterns without announcing the solution. Weeks 23–24 emphasize spoken mock
interviews and changed-constraint follow-ups. Advanced enrichment should not displace weak core
patterns; use the existing weekly gates to decide where repetition is needed.

Every seventh day re-solves two earlier LeetCode companions or their local equivalents. Use
5 minutes recall, 20 minutes per attempt, 10 minutes critique and 5 minutes logging. Select
unfinished work instead of adding extra tasks. A harder problem may consume both attempt slots.

## Evidence and completion

For an online attempt, record problem number, actual result, approach, complexity, tests and
hints in NOTES.md. A link to your submission is useful if available; do not claim acceptance
without submitting. Explain differences from the local contract. For a local attempt, run
`python course.py practice N` and add boundary cases. That command does not submit to LeetCode
and does not verify the online judge interface. Track either route honestly; cold re-solves
and the weekly rubric matter more than accepted-count totals.

## References

The official [Top Interview 150](https://leetcode.com/studyplan/top-interview-150/) and
[LeetCode 75](https://leetcode.com/studyplan/leetcode-75/) are supplementary interview collections.
This course uses its own prerequisite order and includes related variants beyond those lists.
See the [day-by-day index](LEETCODE_INDEX.md) for actual assigned problems and access notes.
