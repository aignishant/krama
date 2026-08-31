---
day: 106
track: practice
title: "Practice — Binary search trees: the ordering property"
status: written
---

# Day 106 · Practice

**DSA topic:** Binary search trees: the ordering property
**System design topic:** Sharding, part one: choosing the key

---

## Code these, in this order

One rule for the whole set: **say the invariant out loud before each problem, using the word "subtree".**
If you catch yourself saying "the left child", stop and say it again properly. That habit is what day 108
is going to test.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Search in a Binary Search Tree | LeetCode 700 (Easy) | One comparison discarding a subtree; write it iteratively. |
| 2 | Convert Sorted Array to BST | LeetCode 108 (Easy) | Why taking the middle prevents the degenerate case. |
| 3 | Range Sum of BST | LeetCode 938 (Easy) | Skipping whole subtrees using the ordering. |
| 4 | Kth Smallest Element in a BST | LeetCode 230 (Medium) | Inorder as sorted order, and stopping early. |

### On problem 1, write it both ways and pick

Recursive and iterative. Say why the iterative version is preferable here, in terms of what happens on
the way back up.

### On problem 2, then build the bad tree

After building the balanced one, insert the same sorted array one value at a time into an empty BST.
Print both heights. Record the two numbers.

### On problem 3, prove the pruning

Add a counter for nodes visited. Compare against a version that visits everything and filters. Run it on
a 1,000-node BST with a narrow range and record both counts.

### On problem 4, do it iteratively and say why

Say what the recursive version would do that you do not want, and give the complexity in terms of
`height` and `k`.

---

### The invariant drill

1. State the invariant using the word "subtree".
2. State it again as a range inherited from ancestors.
3. State it a third time in terms of inorder traversal.
4. Say why all three are the same statement.

### The classic-error drill

1. Build the tree with an 8 in the right subtree of 10.
2. Print its inorder traversal and say what is wrong with it.
3. Run `search` for 8 and record the result.
4. Run an exhaustive search for 8 and record the result.
5. Say in one sentence why this bug is hard to debug.

### The ranges drill

1. Draw a seven-node BST and label every node with its permitted range.
2. Say what happens to the range when you go left, and when you go right.
3. Say which ancestor sets each bound for a node two levels down.
4. Say why "check the parent" is not enough.

### The what-it-buys drill

1. Write `search` in four lines.
2. Say what a single comparison eliminates.
3. Give the comparison count for a balanced million-node BST.
4. Give it for the same values in a plain binary tree, and for a chain.

### The balance drill

1. Insert 1 to 7 in order and give the height.
2. Insert them middle-first and give the height.
3. Say what this proves about what determines a tree's shape.
4. Say what the expected height of a randomly built BST is.
5. Say why sorted input is the common case, not the exotic one.

### The against-alternatives drill

1. Fill in the comparison table for sorted array, hash map and balanced BST.
2. Give four operations a hash map cannot do.
3. State the one-sentence rule for choosing between them.
4. Compute an insertion into a million-element sorted array against a balanced BST.
5. Give the memory ratio between a BST and a sorted list of the same values.

### The duplicates drill

1. Name the four conventions.
2. Say which one most problems assume and which one you would build.
3. Say what goes wrong if equal values are allowed on both sides.
4. Write the counting node and the `add` method.

### The break-it drill

Trigger each and record the exact output or error:

1. `search` on the locally-correct, globally-broken tree.
2. Inserting a string into a tree of integers.
3. Inserting 1 to 10,000 in order, then recursing over the result.
4. Allowing duplicates left in one function and right in another, then searching.
5. Using a BST where a hash map would do — state what you lost.

---

### The two-techniques drill

1. Define replication and sharding in one line each.
2. Say which scales reads and which scales writes.
3. Say why they are orthogonal and what a real deployment does.
4. Say why replication has a hard ceiling.

### The choosing drill

1. State the one question that chooses the shard key.
2. Name the four requirements a key must satisfy.
3. For each requirement, give a key that fails it and say how.
4. Choose a key for: a social feed, a chat app, multi-tenant SaaS, an orders table.

### The strategies drill

1. Name all four strategies.
2. For each, give one thing it makes fast and one it makes terrible.
3. Say which one multi-tenant systems use and why.
4. Say which one is sometimes a legal requirement.

### The hotspot drill

1. Describe the append hotspot in two sentences.
2. Compute the load distribution for 10,000 writes/s over 4 range shards on a timestamp.
3. Say what the effective capacity is, and what it cost.
4. Give the composite-key fix and name the database whose data model is built on it.
5. Say why hashing does not fix skew in *activity*, and give the social-product example.

### The what-breaks drill

1. Name the three permanent losses.
2. For each, give the workaround and its cost.
3. Say what happens to auto-increment ids, and name the standard fix.
4. Say what co-location means and give a concrete example.
5. Say what you do with small reference tables.

### The scatter-gather drill

1. Describe a scatter-gather.
2. Say why its latency is the maximum rather than the average.
3. Compute the probability that at least one of 16 shards is slow, given a 10 ms p99.
4. Compute the availability of a 16-shard fan-out at 99.9% each.
5. Name three ways to avoid serving such a query from the shards.

### The when-not-to drill

1. Give three situations where you would not shard, and what you would do instead.
2. State the write rate and data size that justify it.
3. Say what the real cost of sharding is, and why it is not the migration.
4. Estimate the calendar cost of changing a shard key later.

### The failure drill

For each, say what happens and what you would add:

1. The table is sharded by `created_at`.
2. Someone asks for "all orders placed today".
3. Two shards issue the same order number.
4. A user changes the field you sharded by.
5. One tenant grows to ten times every other tenant.
6. A migration is applied to 15 of 16 shards.

One of the six has no clean fix. Name it and say what you must do at design time instead.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *What makes a tree a binary search tree?*
   The invariant with the word "subtree", the range formulation, inorder as the third statement, what one
   comparison buys, the immediate qualification that it is `O(height)` not `O(log n)`, and when you would
   use a hash map instead.

2. *How would you shard this table? What breaks after you do?*
   Sharding separated from replication, the question that chooses the key, the key with all four reasons,
   hash with the append-hotspot justification, co-location, then the three permanent losses plus ids, and
   the query you have just made expensive.

3. *What is the worst case for a BST, and how do real systems avoid it?*
   The chain from sorted insertion, why sorted input is normal, the expected height of a random tree, and
   self-balancing plus B-trees.

---

## Before you move on

- [ ] I state the invariant using the word "subtree", every time.
- [ ] I can give all three equivalent formulations.
- [ ] I built the broken tree and saw `search` fail to find a value that is present.
- [ ] I can label a drawn BST with every node's permitted range.
- [ ] I say `O(height)` and then say what determines the height.
- [ ] I know the expected height of a randomly built BST.
- [ ] I can fill in the comparison table against sorted arrays and hash maps.
- [ ] I can name four operations a hash map cannot do.
- [ ] I can state a duplicates policy and say what breaks without one.
- [ ] I know why the shape depends on insertion order, with the two heights to prove it.
- [ ] I can separate replication from sharding in one line each.
- [ ] I can state the question that chooses the shard key.
- [ ] I can name the four requirements and a key that fails each.
- [ ] I can describe the append hotspot with the load arithmetic.
- [ ] I know the composite-key fix and the database built on it.
- [ ] I can name the three permanent losses and the id problem.
- [ ] I can compute scatter-gather latency and availability for 16 shards.
- [ ] I can say when I would not shard, and what I would do instead.
- [ ] I answered all three questions above out loud.
