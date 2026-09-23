# Hints — Merge overlapping intervals

Open only after an independent attempt. These guide the mechanism without supplying a solution.

<details><summary>Hint 1 — representation</summary>

Sort by start and maintain one active interval.

</details>

<details><summary>Hint 2 — proof obligation</summary>

Write the state immediately before an update and immediately after it. Identify which discarded
possibilities can no longer improve the answer. For recursive/DP tasks, state the subproblem
and why every dependency is smaller or already available.

</details>

<details><summary>Hint 3 — targeted debugging</summary>

Find the smallest valid input on which your baseline and optimized versions disagree. Compare
their state traces at the first divergence, including equality, initial state and final cleanup.
Recheck the contract before changing the algorithm.

</details>
