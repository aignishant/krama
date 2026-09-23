---
day: 134
track: practice
title: "Practice — Topological sort"
status: written
---

# Day 134 · Practice

**DSA topic:** Topological sort
**System design topic:** Blob storage versus storing files in the database

---

## Code these, in this order

One rule for the whole set: **write the edge's meaning as an English sentence in a comment before writing the
append.** "An edge from A to B means A must happen before B." Then check by hand, on a two-vertex example,
which adjacency list gets the entry. Reversing it is silent, and it is the most common failure on this family.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Course Schedule II | LeetCode 210 (Medium) | Kahn's, returning the order, and building from `range(n)`. |
| 2 | Alien Dictionary | LeetCode 269 (Hard) | The modelling: adjacent pairs, first difference, prefix case. |
| 3 | Minimum Height Trees | LeetCode 310 (Medium) | Kahn's on an undirected graph, peeling degree-1 leaves. |
| 4 | Sequence Reconstruction | LeetCode 444 (Medium) | Is the order **unique**? One extra check inside the loop. |
| 5 | Parallel Courses III | LeetCode 2050 (Hard) | Longest path in a DAG — one pass in topological order. |
| 6 | Sort Items by Groups Respecting Dependencies | LeetCode 1203 (Hard) | Two topological sorts, nested. |

### On problem 1, write both algorithms

Kahn's and reversed DFS finish order. Verify that both outputs are valid using a property check — for every
edge `(a, b)`, `position[a] < position[b]` — rather than comparing them to each other. They will differ.

### On problem 1, break it three ways

1. Reverse the edge direction. Record the output and verify it against the property check.
2. Build the adjacency from the edge list instead of `range(n)`, with an isolated vertex present. Record the
   result and say why it is a phantom cycle.
3. In the DFS version, move the append before the loop. Record the output on `0→1`, `2→1`.

### On problem 2, list the three input rules

Before coding: adjacent pairs only, first difference only, and the prefix case. Write each as one line. Then
solve it. The prefix case is the hidden test.

### On problem 5, notice what changed

The answer is not an order, it is a length. Write down the one-line recurrence and say why processing in
topological order means every dependency's answer is already final when you need it.

### Then build the parallel scheduler

Take your problem 1 solution and return levels instead of a flat list. Then print:

1. The number of levels — the critical path.
2. The widest level — the maximum useful worker count.
3. The total number of tasks.

Three numbers, and say what each tells a user.

---

### The definition drill

1. Define a topological order in one sentence.
2. Say exactly when one exists.
3. Say why there are usually many, and what that means for tests.
4. Write the five-line property check that verifies any candidate order.

### The Kahn's drill

1. Write it from memory.
2. Say what in-degree means, in domain words.
3. Say what the decrement represents.
4. Say what `len(order) != n` means and why the leftovers are stuck.
5. Give four reasons to prefer it over DFS.

### The DFS drill

1. Write it from memory, including the colour check.
2. Say where the append goes and why.
3. Say why reversing the finish order gives a valid order.
4. Say what happens without the cycle check.
5. Give the one situation where you would prefer it.

### The variants drill

1. Turn Kahn's into a parallel schedule and name the two numbers it produces.
2. Turn it into the lexicographically smallest order and give the cost.
3. Give the one-sentence reason the greedy choice is correct.
4. Add the uniqueness check and say where it goes.
5. Say how you compute the longest path in a DAG with the same pass.

### The costs drill

1. Give time and space for Kahn's and for DFS.
2. Give the cost of the heap version and the ratio at `V = 100,000`.
3. Say what counting all valid orders costs, and give an example that explodes.
4. Give the recursion caveat and the input size at which it bites.
5. Compute the critical path win for 1,000 tasks, 5 s each, 12 levels.

### The break-it drill

Trigger each and record the exact output or error:

1. Edge direction reversed, verified with the property check.
2. Adjacency built from edges only, with an isolated vertex.
3. DFS append before the loop, on `0→1`, `2→1`.
4. DFS with no cycle check, on a triangle.
5. A test asserting one specific order, with adjacency built in a different order.
6. Recursive DFS on a 100,000-long chain.

---

### The four-numbers drill

1. Compute backup and restore time for 20 GB of rows and 4 TB of blobs, both ways.
2. Compute buffer-pool turnover for a 16 GB pool at 100 blob reads a second.
3. Compute connection occupancy for 200 concurrent 50 MB downloads.
4. Compute monthly cost for 4 TB in each store, including backup storage.
5. Say which of the four is the one that shows up as "the database got slow".

### The two-systems drill

1. Name the two problems the external store creates.
2. Give the write order that makes failures recoverable, and say why.
3. Say what happens if you reverse that order.
4. Describe the reconciliation job and its three outputs.
5. Say which of the three is the alarming one and why.

### The deletion drill

1. Name the four systems a delete touches.
2. Give the soft-delete-then-clean-up pattern.
3. Say what makes the cleanup job safe to retry.
4. Say what changes when there is a regulatory deletion requirement.

### The minority-case drill

1. Give the three situations where the database is the right answer.
2. Give the size and volume thresholds, roughly.
3. Say what TOAST does and which argument it neutralises.
4. Say which arguments TOAST does **not** affect.
5. Give SQLite's benchmark result and why it holds.

### The migration drill

1. Give the four steps of migrating 4 TB of blobs out of a database.
2. Say what "null the column" does and does not reclaim.
3. Say what a `VACUUM FULL` on 4 TB costs.
4. Name the four metrics you would measure before and after.

### The trade-offs drill

1. Say what object storage costs you, in two words, and expand each.
2. Say what the database costs you at scale — six things.
3. Give the argument that settles it for anything user-facing.
4. Give the rough crossover in terms of blob bytes versus row bytes.
5. Name the case where neither is right.

### The failure drill

For each, say what happens and what you would build:

1. The object uploads and the row insert fails.
2. The row is created after the object, and the process dies in between.
3. A `READY` row whose object is missing.
4. A 4 TB database restore during an outage.
5. A hundred concurrent 50 MB downloads through the application.
6. A `SELECT *` on a table with 4 MB blobs, run by a reporting tool.
7. Nulling a blob column on 4 TB and expecting the disk to free up.

Two of the seven are data loss and five are performance. Sort them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Order these tasks so that every dependency comes first.*
   The edge meaning as a sentence, Kahn's with the in-degree explanation, `len(order) != n` as the cycle test,
   the four reasons to prefer it, and the parallel-schedule variant offered before being asked.

2. *Give me a valid course order, and tell me if it is impossible.*
   One pass, both answers, and the two silent bugs — reversed direction and building from the edge list —
   named before you write them.

3. *Should the images go in the database? Defend your answer.*
   The four numbers, then what the external store costs you — no transaction across two systems — then the
   ordering rule and the reconciliation job, then where the answer flips.

---

## Before you move on

- [ ] I write the edge's meaning as a sentence before the append.
- [ ] I can define a topological order and say exactly when one exists.
- [ ] I verify orders with a property check, not by comparing to a fixed list.
- [ ] I can write Kahn's from memory.
- [ ] I can explain in-degree and the decrement in domain words.
- [ ] I know `len(order) != n` is the cycle test and why.
- [ ] I can give four reasons to prefer Kahn's.
- [ ] I can write the DFS version, including the colour check.
- [ ] I know the append goes after the loop and why.
- [ ] I know what happens to DFS without the cycle check.
- [ ] I can produce a parallel schedule and name its two numbers.
- [ ] I can produce the lexicographically smallest order and justify the greedy choice.
- [ ] I can add the uniqueness check.
- [ ] I know how to compute the longest path in a DAG with one pass.
- [ ] I know counting all orders is exponential.
- [ ] I build from `range(n)` and know it prevents a phantom cycle.
- [ ] I can compute backup and restore times both ways.
- [ ] I can explain buffer-pool damage and why it hits *other* queries.
- [ ] I can compute connection occupancy for large downloads.
- [ ] I can quote the cost per gigabyte both ways.
- [ ] I can name the two problems the external store creates.
- [ ] I know to create the row first, and what reversing that costs.
- [ ] I can describe the reconciliation job and its alarming output.
- [ ] I can give the soft-delete-then-clean-up deletion pattern.
- [ ] I can name the three cases where the database is right.
- [ ] I know what TOAST fixes and what it does not.
- [ ] I can give the migration steps and the vacuum caveat.
- [ ] I know the argument that settles it for user-facing files.
- [ ] I answered all three questions above out loud.
