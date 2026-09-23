---
day: 104
track: practice
title: "Practice — Path problems, and the return-value trick"
status: written
---

# Day 104 · Practice

**DSA topic:** Path problems, and the return-value trick
**System design topic:** Database replication

---

## Code these, in this order

One rule for the whole set: **before writing anything, say which kind of path is meant** — root-to-leaf,
strictly downward, or any-to-any with a bend. Three different problems, three different shapes, and the
question rarely says which.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Path Sum | LeetCode 112 (Easy) | The leaf test, and state carried down as an argument. |
| 2 | Binary Tree Paths | LeetCode 257 (Easy) | Collecting paths, and why passing a string needs no undo. |
| 3 | Path Sum III | LeetCode 437 (Medium) | Prefix sums on a tree, and the un-choose on the map. |
| 4 | Binary Tree Maximum Path Sum | LeetCode 124 (Hard) | Record versus return, the floor, and the `-inf` start. |

### On problem 1, use the wrong leaf test first

Write the base case as `if node is None: return remaining == 0`. Run it on `[1, 2]` with target 1 and
record the answer. Then say what a leaf actually is.

### On problem 3, write both versions and time them

Write the naive start-from-every-node version, then the prefix-sum one. Time both on a chain of 2,000
nodes and record the ratio. Then delete `seen[running] -= 1` and say what the count does and why.

### On problem 4, break it three ways

Run each and record: return the bent value to the parent; drop the `max(0, ...)`; start `best` at 0. Say
which inputs expose each one, and whether any of them raises.

### After all four, fill in the table

For each problem: what is returned to the parent, what is recorded on the side, and whether there is a
floor. If you can produce that from memory, you have the technique.

---

### The definition drill

1. Name the three meanings of "path" and give a LeetCode number for each.
2. Say which traversal each one uses and which direction information travels.
3. Say which one has no floor, and why not.
4. Write the question you would ask the interviewer, in one sentence.

### The leaf drill

1. Write the correct leaf test.
2. Say what `node is None` reports on a one-sided node.
3. Give the input and target where the wrong test differs, with both answers.
4. Say why this trap is specific to root-to-leaf problems.

### The record-versus-return drill

1. Write the two lines and label them.
2. Say the sentence explaining why the parent cannot use the recorded value.
3. Merge them into one return and describe how the answer misbehaves.
4. Fill in the family table for five problems.

### The floor drill

1. Write the floor and say what it means in one sentence.
2. Run `[5, -100, 3]` with and without it and record both answers.
3. Say which array algorithm this is the same idea as.
4. Say why root-to-leaf problems must not have it.

### The `-inf` drill

1. Say what the floor applies to and what it does not.
2. Run `[-3]` with `best = 0` and record the answer.
3. Say why 0 is not a valid answer for that tree.
4. State the rule in one line.

### The prefix-sum drill

1. Write the path-sum-III solution from memory.
2. Say what `seen[0] = 1` is for, and which earlier day it comes from.
3. Say what the un-choose keeps out of the map, and why that matters.
4. Say what the map's size is bounded by, and why it is not `O(n)`.
5. Give the complexity of both versions on a balanced tree and on a chain.

### The break-it drill

Trigger each and record the exact output:

1. `node is None` as the leaf test, on a one-sided tree.
2. Returning the bent value to the parent.
3. No floor, on `[5, -100, 3]`.
4. `best = 0`, on an all-negative tree.
5. Missing `seen[running] -= 1`.
6. Missing `seen[0] = 1`.
7. String concatenation down a 5,000-node chain, timed.

### The extension drill

1. Modify max path sum to return the path.
2. State what the space becomes and why.
3. Describe the two-pass alternative that keeps `O(height)`.
4. Say what `all_path_sums` costs in output size for a perfect million-node tree.

---

### The topology drill

1. Draw leader-follower and state the invariant in one sentence.
2. Say what travels between them, and in what property.
3. Name the three replication formats and give the danger of the first.
4. Name the two other topologies and say when each is worth it.

### The durability drill

1. Define asynchronous, synchronous and semi-synchronous.
2. Say what each one loses and what each one costs.
3. Say why fully synchronous makes followers a liability.
4. Compute the writes at risk at 1,000 writes/s with 200 ms and 5 s of lag.
5. Give the latency figures for a synchronous follower in the same AZ, another AZ, another region.

### The failover drill

1. Name the five steps in order.
2. Say which step people skip and what it causes.
3. Say which step is often the slowest, and what to use instead.
4. Compute a realistic RTO from the components.
5. Define RPO and RTO in one sentence each, and say what each depends on.

### The split-brain drill

1. Describe the failure in two sentences.
2. Say why it cannot be automatically repaired.
3. Name the three defences and say what each one does.
4. Say why cluster sizes are odd.
5. Give the one-sentence rule from the brothers' ledger.

### The not-a-backup drill

1. Say what replication protects against and what it does not.
2. Give the specific statement that replication faithfully copies.
3. Name what you need instead, and what it consists of.
4. Describe the delayed-follower trick and what window it buys.

### The numbers drill

Compute or state each:

1. Typical lag in the same data centre, cross-region, and during a bulk load.
2. Writes at risk for two different lag figures.
3. A realistic automated RTO, broken down by component.
4. Time to build a new follower for a 2 TB database over 1 Gbit/s.
5. Why four nodes tolerate no more failures than three.

### The failure drill

For each, say what happens and what you would add:

1. The synchronous follower goes down.
2. A schema migration locks a table on the leader.
3. Clients find the leader through DNS with a 60-second TTL.
4. A batch job writes ten million rows.
5. Someone runs `DELETE FROM orders` with no `WHERE`.
6. Someone suggests adding a replica to fix an ongoing overload.

Two of the six are not solved by replication at all. Name them and say what solves them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the maximum path sum in the binary tree.*
   The definition of path pinned down first, the one-highest-node observation, record versus return said
   precisely with the reason the parent cannot use the bend, the floor with its Kadane connection, the
   `-inf` initialisation with the reason, and both complexities.

2. *How do you make the database survive a machine failure?*
   Leader-follower with the one-writer invariant, an ordered change log in row format, semi-synchronous
   with the writes-at-risk arithmetic, the five failover steps with fencing named, RPO and RTO given as
   numbers, and replication distinguished from backup.

3. *The old leader comes back. Then what?*
   Split-brain described, why it cannot be auto-repaired, and the three defences with what each one does.

---

## Before you move on

- [ ] I ask which kind of path is meant before writing anything.
- [ ] I can write the correct leaf test and say what the wrong one does.
- [ ] I can say the record-versus-return sentence precisely.
- [ ] I know why the parent cannot use the recorded value.
- [ ] I can write the floor and say what it means in plain words.
- [ ] I know that the floor applies to the arms and not the answer.
- [ ] I ran `[-3]` with `best = 0` and know what it returns.
- [ ] I can write path sum III with prefix sums from memory.
- [ ] I know what the un-choose on the map keeps out, and the bound it gives.
- [ ] I can fill in the family table for five problems.
- [ ] I can state the leader-follower invariant in one sentence.
- [ ] I can name the three replication formats and the danger of statement-based.
- [ ] I can define all three durability levels and say which one is actually used.
- [ ] I can compute writes at risk from a write rate and a lag.
- [ ] I can name the five failover steps and say which one people skip.
- [ ] I can define RPO and RTO and give realistic numbers for both.
- [ ] I can describe split-brain and name three defences.
- [ ] I can say why replication is not a backup, with the specific example.
- [ ] I answered all three questions above out loud.
