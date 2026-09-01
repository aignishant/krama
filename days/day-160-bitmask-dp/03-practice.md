---
day: 160
track: practice
title: "Practice — Bitmask DP"
status: written
---

# Day 160 · Practice

**DSA topic:** Bitmask DP
**System design topic:** Design Google Drive or Dropbox

---

## Code these, in this order

One rule for the whole set: **before choosing the dimensions, ask out loud whether the order matters or only
the set.** That one question decides between `dp[mask]` and `dp[mask][last]`, and getting it wrong returns a
plausible smaller number with no error at all.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Travelling Salesman | classic — write it yourself | `dp[mask][last]`, and the trip home. |
| 2 | Assignment problem | classic — write it yourself | `popcount` as the implicit second index. |
| 3 | Partition to K Equal Sum Subsets | LeetCode 698 (Medium) | Bitmask over items, with pruning that matters. |
| 4 | Shortest Path Visiting All Nodes | LeetCode 847 (Hard) | Bitmask plus BFS, and multiple start states. |
| 5 | Find the Shortest Superstring | LeetCode 943 (Hard) | TSP in disguise, with overlap as the distance. |
| 6 | Number of Ways to Wear Different Hats | LeetCode 1434 (Hard) | Masking the smaller dimension, deliberately. |

### On problem 1, drop the trip home

Return `min(dp[full])` instead of `min(dp[full][last] + dist[last][0])`. Run on the four-city example and
record both. **Say which problem each one solves**, and why neither raises an error.

### On problem 1, use `dp[mask]` alone

Try it without the `last` dimension. Run it and record the answer against the correct one. **Say in one
sentence what the algorithm is effectively allowed to do**, and why that produces a smaller number.

### On problem 1, measure the ceiling

Time your solution at `n = 10`, `12`, `14`, `16`. Record all four. **Extrapolate to `n = 20`** and say whether
you would submit it. Then compute the memory for `n = 24` and say what fails first.

### On problem 2, remove the `popcount` trick

Add an explicit `job` dimension: `dp[mask][job]`. Confirm it agrees. **Then say why the extra dimension is
redundant**, in one sentence about what the mask already tells you.

### On problem 2, look up the Hungarian algorithm's complexity

Write both complexities down. Compute the operation counts at `n = 20` and at `n = 200`. **Say what you would
actually tell an interviewer** about your bitmask solution.

### On problem 3, add pruning and measure

Solve it first with no pruning, then add: sort descending, skip if the current subset would overflow, and skip
equal values already tried. Time each version on `[4,3,2,3,5,2,1]` with `k = 4` and on a harder 16-element
input. **Record the ratios.**

### On problem 5, find the distance function

Before coding, say what "distance from string A to string B" means here. **Then notice the problem is TSP with
an open path**, and say which line of your day-1 solution changes.

### Then the submask drill

Implement `all_submasks` and verify it yields exactly `2^k - 1` results for a mask with `k` bits set, on twenty
random masks. Then time the total work over all masks for `n = 12` and `n = 16`, and **compare against the
naive `4^n` version.** Say which power you measured.

### Then the bit-operation drill

Write all five operations from memory. Then write `mask & -mask` and `mask & (mask - 1)` and say what each
does. **Then time `bin(m).count("1")` against `m.bit_count()`** and record the ratio.

---

### The encoding drill

1. Give all five operations from memory.
2. Give the full mask for `n` and say why it is not `1 << n`.
3. Say what `mask & -mask` isolates and what `mask & (mask-1)` removes.
4. Say why the shift must be parenthesised, with the failing example.

### The state drill

1. State the test that decides `dp[mask]` versus `dp[mask][last]`.
2. Say why the assignment problem needs only one dimension.
3. Say why TSP needs two.
4. Say what happens if you use one where you need two — and whether it errors.

### The fill-order drill

1. Say why ascending mask order is correct.
2. Say whether that holds for both the push and the pull pattern.
3. Say what happens if you mix the two patterns in one loop.
4. Contrast with interval DP in one sentence.

### The TSP drill

1. Give the state and the base case.
2. Give the transition.
3. Give the answer line, including the term people forget.
4. Say what the open-path version solves instead.
5. Say what reconstruction needs beyond parent pointers.

### The ceiling drill

1. Give the state count and the work per state.
2. Fill in the table for `n = 15, 20, 24, 30`.
3. Say what fails first in Python and at what `n`.
4. Give the brute-force comparison at `n = 20` and at `n = 25`.
5. Say both halves of what bitmask DP buys.
6. Say what exists instead when `n` is genuinely large.

### The submask drill

1. Give the idiom from memory.
2. Explain why `(submask - 1) & mask` lands on the next submask.
3. Say why the total is `3^n` and not `4^n`, in one sentence about three states.
4. Give the comparison at `n = 16`.
5. Say what the loop as written omits.
6. Say what `n` submask problems top out at, and why it is lower.

### The break-it drill

Trigger each and record the exact output or error:

1. Missing the trip home in TSP.
2. `dp[mask]` alone for TSP.
3. `mask & 1 << 1 == 2`.
4. `mask - (1 << i)` where bit `i` is not set.
5. `1 << n` used as the full mask.
6. `n = 24` allocation.
7. `bin(m).count("1")` in the inner loop.

Five of the seven give no error at all. Name them.

---

### The framing drill

1. Say what makes this design different from the others this week.
2. Give the change rate and say what it means for the design.
3. Say what the actual difficulty is.

### The chunking drill

1. Describe the data model in two sentences.
2. Give the upload protocol in three steps.
3. Compute what a one-paragraph edit to a 50 MB file uploads.
4. Say what fixed boundaries do on an insertion, and why.
5. Describe content-defined chunking and what picks a boundary.

### The sync drill

1. Say why polling every file fails, with numbers.
2. Say why timestamps are the wrong comparison.
3. Describe the cursor protocol and what one request returns.
4. Say why the sequence only needs to be monotonic per user.
5. Say why the notification carries no data.
6. Say why the cursor is saved after applying, not before.
7. Say what response the protocol needs for a very old cursor.

### The conflict drill

1. Say how a conflict is detected, and what is not used.
2. Give the three options and what each costs.
3. Say why last-write-wins is wrong rather than merely simple.
4. Say why merging is impossible in general.
5. Say what the honest design's own failure mode is.
6. Say what Google Docs does instead, and why it is a different question.

### The dedup drill

1. Give the storage saving, personal and corporate.
2. Describe the information leak, as a concrete attack.
3. Describe the worse version of the attack.
4. Give three defences and say which you would take.
5. Say what residual leak remains, and whose decision it is.

### The sizing drill

1. Compute the storage before and after dedup.
2. Compute the bandwidth saving from delta sync, including the device multiplier.
3. Say what is surprising about the metadata.
4. Compute the change log growth and say what compaction is for.
5. Give the sync latency budget and say what dominates it.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the shortest route visiting every city once and returning to the start.*
   The set-versus-order test, the two-dimensional state and why, the base case, the answer line with the trip
   home, the complexity, and both halves of what it buys.

2. *How large can `n` be, and can you do better?*
   The state table, what fails first in Python, the brute-force comparison, why NP-hardness means no, and what
   exists instead — including the Hungarian algorithm for the assignment case.

3. *Design Dropbox.*
   Why the difficulty is not scale, chunks and content-defined boundaries, the cursor protocol with its three
   details, conflicts by base version with both copies kept, and the dedup information leak.

---

## Before you move on

- [ ] I can write all five bit operations from memory.
- [ ] I know the full mask is `(1 << n) - 1`.
- [ ] I always parenthesise the shift, and know the failing example.
- [ ] I ask whether order matters or only the set, before choosing dimensions.
- [ ] I know why the assignment problem needs one dimension.
- [ ] I know why TSP needs two, and what one dimension silently allows.
- [ ] I know ascending mask order is a correct fill order, and why.
- [ ] I can write TSP including the trip home.
- [ ] I know what the open-path version solves instead.
- [ ] I can reconstruct the route, undoing the mask as I go.
- [ ] I can fill in the `2^n` ceiling table.
- [ ] I know memory fails before time in Python, and at what `n`.
- [ ] I can give the brute-force comparison at `n = 20`.
- [ ] I say both halves: enormous improvement, still exponential.
- [ ] I know what exists instead when `n` is large.
- [ ] I know the Hungarian algorithm is polynomial, and would volunteer it.
- [ ] I can write the submask idiom from memory.
- [ ] I can explain why the total is `3^n`.
- [ ] I know submask problems top out lower than `2^n` ones.
- [ ] I know why the Dropbox difficulty is correctness, not scale.
- [ ] I can describe the chunk model and the upload protocol.
- [ ] I know what fixed boundaries do on an insertion.
- [ ] I can explain content-defined chunking.
- [ ] I can describe the cursor protocol and why polling fails.
- [ ] I know the notification carries no data, and why.
- [ ] I know the cursor is saved after applying, and why.
- [ ] I know conflicts are detected by base version, not timestamps.
- [ ] I know why keeping both copies is the honest answer.
- [ ] I can describe the dedup information leak as an attack.
- [ ] I can give three defences and pick one.
- [ ] I answered all three questions above out loud.
