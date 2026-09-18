# DSA practice contract

This is a broad interview-oriented course. Advanced range queries, matching, bitmask DP and
tree rerooting provide breadth; deep competitive programming, geometry, FFT and advanced flow
are outside the core. A one-hour daily budget prioritizes one serious problem over a problem quota.

## What each section contains

Every core day supplies an original problem contract, JSON example, target complexity, unsolved
function, executable fixture test, staged hints, boundary-test instructions and evidence notes.
The statement is self-contained; no external judge account is required. Review days deliberately
repeat earlier problems and should not be counted as new problems.

## How to solve

1. Name the input size and clarify the contract.
2. Describe a slow correct baseline; do not optimize an undefined problem.
3. State the invariant or recurrence and trace one example.
4. Attempt independently, then use one hint if stuck.
5. Implement, run fixtures, and add four cases chosen to attack assumptions.
6. Use a small brute-force oracle or metamorphic property when appropriate.
7. Explain correctness, complexity, mutation and output ordering.
8. Keep the smallest failing input in the mistake ledger.

For lists test boundaries, duplicates and order. For trees test empty/skewed/balanced shapes when
allowed. For graphs test disconnected regions, self-loops only if allowed, cycles and unreachable
targets. For DP test base states, impossible states and zero-valued choices. For cache designs
test updates, repeated access, eviction ties and minimum capacity. A sample passing is insufficient.

## Weekly rubric

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Correctness | Cannot finish baseline | Needs hints or misses a case | Independently correct with tests |
| Explanation | Cannot state why | Describes steps | States and defends invariant/recurrence |
| Complexity | Wrong or missing | Mostly right | Accounts for relevant operations and space |
| Tests | Sample only | Some boundaries | Adversarial cases plus a demonstrated failure |

Pass at 6/8 or above with correctness=2. Otherwise mark needs-review and use the next review
session. More than two unresolved core problems means pause that track's new content. Optional
extensions and bonus readings are the first things to drop. Retention matters more than a streak.
