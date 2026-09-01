---
day: 161
track: practice
title: "Practice — Space optimisation in DP"
status: written
---

# Day 161 · Practice

**DSA topic:** Space optimisation in DP
**System design topic:** Design Uber

---

## Code these, in this order

One rule for the whole set: **write the full table first, get it right, then collapse it.** A wrong recurrence
in a table can be printed and inspected; a wrong recurrence in an array that is half one row and half another
tells you almost nothing. **Correctness first, then space.**

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Climbing Stairs | LeetCode 70 (Easy) | The two-variable collapse, and simultaneous assignment. |
| 2 | Unique Paths | LeetCode 62 (Medium) | One row, and naming which half is which. |
| 3 | Edit Distance | LeetCode 72 (Medium) | One row plus the diagonal variable. |
| 4 | Partition Equal Subset Sum | LeetCode 416 (Medium) | The backwards inner loop, and why. |
| 5 | Minimum Falling Path Sum | LeetCode 931 (Medium) | Where the collapse is impossible in place. |
| 6 | Longest Common Subsequence | LeetCode 1143 (Medium) | Length in linear space; then the string. |

### On problem 1, write it without simultaneous assignment

Use two statements and no temporary. Run for `n = 6` and record the answer against 8. **Say what sequence it
actually computed.**

### On problem 2, print the array mid-pass

Stop the loop at column 4 of row 2 and print `row`. **Mark which entries are the previous row and which are
the current one.** Then say why `row[c] += row[c-1]` is exactly "above plus left".

### On problem 3, leave out `row[0] = i`

Run on `"horse"` and `"ros"` and record the answer against 3. **Say what the algorithm now believes about
turning a string into nothing.**

### On problem 3, use `row[j-1]` as the diagonal

Run on `"intention"` and `"execution"` and record the answer against 5. **Say which generation of the data it
read**, and why the failure is invisible on many inputs.

### On problem 4, reverse the inner loop

Run the forwards version on `[3]` with target 9 and record the answer. Then run both versions on `[1, 2, 5]`
with target 8 and record those. **Say why the second test passes under both**, and what that means for how you
choose test inputs.

### On problem 5, collapse it in place anyway

Update the row in place. Run on `[[2,1,3],[6,5,4],[7,8,9]]` and record the answer against 13. **State the
precondition for the one-row trick**, and say which dependency violates it.

### On problem 6, do all three versions

Write the full table with reconstruction, the two-row version, and the one-row version. Confirm all three give
the same length. **Then try to reconstruct from the collapsed one and say precisely what stops you.**

### Then the measurement drill

Time and measure the memory of the full table and the one-row version of problem 2 at 2,000 × 2,000. Record
both times and both memory figures. **Say which one is faster and why** — the answer is not the one people
expect.

### Then the Hirschberg drill

Read the algorithm once. Then, without looking, say the four steps out loud and give its time and space.
**You are not writing it.** The target is being able to answer "give me the path in linear space" in thirty
seconds.

---

### The rule drill

1. State the rule in one sentence.
2. Give the four shapes and what each keeps.
3. Say which shape has no collapse, and why.
4. Say what the collapse costs in time. (Nothing — say why, and why it can be faster.)

### The one-row drill

1. Say what the array holds during a pass, and where the split is.
2. Say what `row[c]` is and what `row[c-1]` is.
3. Give the precondition for the trick.
4. Name a variant that violates it and say what it needs instead.
5. Say what must be re-established on every row.

### The diagonal drill

1. Say why one row is not enough when the recurrence needs `dp[i-1][j-1]`.
2. Give the three lines that fix it.
3. Say what each of the three does.
4. Say which one is most often forgotten.

### The direction drill

1. Say what backwards guarantees and what forwards allows.
2. Give the two problems and which direction each needs.
3. Give the one-item example that separates them.
4. Say what error either version raises. (None — say what to do instead.)
5. Say what kind of test input would hide the bug.

### The reconstruction drill

1. Say what a collapsed array has lost.
2. State the trade in one sentence.
3. Give Hirschberg's four steps.
4. Give its time and space.
5. Say why the time is exactly double.
6. Say whether you would write it, and what you would say instead.

### The when-not-to drill

1. Give a size at which collapsing is not worth it.
2. Say what it costs in readability and debugging.
3. Say what order you would do things in, in an interview.
4. Say why a memoised solution cannot be collapsed at all.

### The break-it drill

Trigger each and record the exact output or error:

1. Non-simultaneous assignment in the two-variable version.
2. Missing `row[0] = i` in the collapsed edit distance.
3. `row[j-1]` used as the diagonal.
4. The forwards loop in 0/1 knapsack.
5. In-place collapse of minimum falling path.
6. Reconstruction attempted from one row.
7. Collapsing interval DP.

Six of the seven give no error at all. Name them.

---

### The split drill

1. Give both halves with their write rates and requirements.
2. Give the ratio between them and say what it means.
3. Say what goes wrong if they share a store.

### The geo drill

1. Say why a B-tree on latitude and one on longitude cannot answer the query.
2. Explain geohashing in two sentences.
3. Say what property makes the prefix scan work.
4. Give the boundary problem and the fix.
5. Say why it fails specifically for the riders you care about.
6. Say why H3 uses hexagons.
7. Say what the exact filter is for.

### The write-rate drill

1. Compute the writes per second.
2. Name the three properties that make it manageable.
3. Compute the size of the live index.
4. Say what the TTL does for free.
5. Say why the global figure is misleading.
6. Say where the historical data goes and why not the query path.

### The cell-size drill

1. Compute the cells in a 3 km radius at 460 m resolution.
2. Say how many candidates that gives downtown.
3. Give the adaptive strategy and why a fixed radius fails.

### The matching drill

1. Say why distance is not the right ranking, with an example.
2. Say why the ETA calls must be batched, with numbers.
3. Give the two-rider example that defeats greedy.
4. Name the problem batched matching actually is, and its complexity.
5. State the cost of batching and whose decision it is.

### The dispatch drill

1. Say what the lock prevents.
2. Say what the TTL prevents, and which message is the one that gets lost.
3. Say what the acceptance handler must re-check, and why.
4. Say what happens on reject and on timeout.

### The trip and pricing drill

1. Say why the transition table is checked on every write.
2. Give the failure it prevents.
3. Describe the surge control loop.
4. Say what the rate limit prevents, and why it is not cosmetic.
5. Say which part of surge is policy rather than engineering.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Can you reduce the space?*
   The rule, the four shapes, what the one-row array holds and where the split is, the precondition, and what
   the collapse costs in time and in reconstruction.

2. *Why does the inner loop go backwards there, and now give me the path in linear space.*
   Which generation each direction reads, the one-item example, and Hirschberg's four steps with its cost.

3. *Design Uber.*
   The two-system split with its ratio, why a normal index fails and what geohashing does, the boundary
   problem and the nine cells, and why greedy matching is wrong.

---

## Before you move on

- [ ] I can state the space rule in one sentence.
- [ ] I know the four shapes and what each keeps.
- [ ] I know which shape has no collapse, and can say why.
- [ ] I can say what the one-row array holds and where the split is.
- [ ] I can point at `row[c]` and `row[c-1]` and name each.
- [ ] I know the precondition: every dependency above or to the left.
- [ ] I can name a variant that violates it.
- [ ] I re-establish the base cases on every row.
- [ ] I know the diagonal trick and its three lines.
- [ ] I know backwards guarantees the previous row.
- [ ] I know forwards allows the current row, and which problem that is.
- [ ] I know neither direction errors.
- [ ] I know the collapse is free in time and can be faster.
- [ ] I know a collapsed array cannot be reconstructed from.
- [ ] I can state that trade in one sentence.
- [ ] I can give Hirschberg's four steps and its cost.
- [ ] I know why its time is exactly double.
- [ ] I know when collapsing is not worth doing.
- [ ] I know a memoised solution must be converted first.
- [ ] I can give the two halves of Uber and their write rates.
- [ ] I know why a normal index cannot answer a radius query.
- [ ] I can explain geohashing and the prefix property.
- [ ] I know the boundary problem and that the fix is nine cells.
- [ ] I know why H3 uses hexagons.
- [ ] I know the exact distance filter is still required.
- [ ] I can name the three properties that make 250,000 writes/s easy.
- [ ] I know the live index is about 200 MB.
- [ ] I know the TTL does offline detection for free.
- [ ] I can give the two-rider example that defeats greedy.
- [ ] I know batched matching is the assignment problem.
- [ ] I answered all three questions above out loud.
