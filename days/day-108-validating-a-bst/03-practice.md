---
day: 108
track: practice
title: "Practice — Validating a binary search tree"
status: written
---

# Day 108 · Practice

**DSA topic:** Validating a binary search tree
**System design topic:** Consistent hashing

---

## Code these, in this order

One rule for the whole set: **write the wrong version first, run it on the killer input, and record the
result.** You cannot claim to have avoided a trap you have never seen fire.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Validate Binary Search Tree | LeetCode 98 (Medium) | The range method, and the counter-example to the local check. |
| 2 | Minimum Absolute Difference in BST | LeetCode 530 (Easy) | Inorder plus a previous value — the same one-variable idea. |
| 3 | Recover Binary Search Tree | LeetCode 99 (Medium) | One or two violations, and which nodes to take from each. |
| 4 | Largest BST Subtree | LeetCode 333 (Medium) | The postorder return-value trick returning four things. |

### On problem 1, run the wrong version first

Write the child-comparison version. Run it on `[10, 5, 15, null, null, 6, 20]` and record what it says.
Then run `search(6)` on that tree and record that too. Then write the correct one.

### On problem 1 again, break the bounds

Write a version seeded with `-2**31` and `2**31 - 1`, and run it on a single node whose value is
`-2**31`. Record the answer and say why it is wrong.

### On problem 3, do both swap shapes

Build a tree with two adjacent values swapped, and another with two non-adjacent values swapped. Print
the inorder sequence for each and count the violations. Say which nodes you take in each case.

### On problem 4, write the naive version first and time it

Check each subtree independently, then do the one-pass version. Time both on a 2,000-node chain and record
the ratio.

---

### The wrong-answer drill

1. Write the child-comparison version from memory.
2. Draw the killer input and say why every pair passes.
3. Say what `search` does on that tree, and why that is the worst kind of wrong.
4. Produce a second, smaller failing input.

### The range drill

1. Write the range version from memory.
2. Say what happens to `low` and `high` on each branch.
3. Label every node of a seven-node tree with its permitted interval.
4. Trace the killer input and say which bound catches the 6, and where that bound came from.

### The sentinel drill

1. Say why `None` is used rather than `INT_MIN`.
2. Give the exact input that breaks the `INT_MIN` version.
3. Name one other value that works, and one reason to prefer `None`.

### The inorder drill

1. Write the inorder version keeping only the previous value.
2. Say why `<=` rather than `<`.
3. Say what the list-building version costs and why you would not write it.
4. Say what the short-circuit saves, with an example.
5. Write the iterative version and say when you would use it.

### The convention drill

1. State the no-duplicates convention and the two comparisons it implies.
2. Change to "duplicates go left" and say which single comparison changes.
3. Run `[2, 2, 2]` through both.
4. Say what you would do in a real implementation instead.

### The recover drill

1. State the one-or-two-violations rule.
2. For an adjacent swap, say which nodes are the culprits.
3. For a non-adjacent swap, say which node you take from each violation.
4. Say why you swap values rather than nodes.
5. State the space complexity and name the `O(1)` variant.

### The break-it drill

Trigger each and record the exact output:

1. The child-comparison version on the killer input.
2. A range version that drops `high` when recursing right.
3. `INT_MIN` as the seed, on a node valued `-2**31`.
4. `<` instead of `<=`, on `[2, 2, 2]`.
5. A module-level `previous` variable, called twice.
6. A recursive validation on a 10,000-node chain.

### The escalation drill

1. Write the naive largest-BST-subtree and say its complexity on a chain.
2. Write the one-pass version and say what the four returned values are.
3. Say what condition makes a node's subtree a BST, in terms of the children's returns.
4. Name the earlier day this shape came from.

---

### The modulo drill

1. Say why `hash % N` breaks when `N` changes, in one sentence about where `N` appears.
2. Give the fraction of keys that move for 4→5, 8→9 and 100→101.
3. Compute the origin load when a cache node is added under plain modulo, at 10,000 reads/s and a 95%
   baseline hit rate.
4. Say why there is no safe intermediate state.

### The ring drill

1. State the four steps of the mechanism.
2. Say what happens to the keys when a node is added, and where they come from.
3. Say what happens when a node is removed.
4. Give the fraction that moves and say why it is the minimum.
5. Draw a ring with four nodes and three keys and assign each key.

### The virtual-nodes drill

1. Give both reasons for virtual nodes.
2. Say which one candidates usually miss.
3. Fill in the table of virtual nodes against spread.
4. Compute what happens to one survivor when a machine dies, with 1 and with 200 virtual nodes, in a
   ten-machine cluster.
5. State the memory and lookup cost of 100 machines at 256 virtual nodes.

### The implementation drill

1. Write `add_node` and `get_node` in outline.
2. Say what data structure holds the positions and what the lookup costs.
3. Name the two implementation details that are bugs rather than preferences.
4. Say why Python's built-in `hash()` must not be used, and what to use instead.
5. Say how replication falls out of the ring, and what "distinct" means there.

### The limits drill

1. Say whether consistent hashing solves hot keys, and why.
2. Name the refinement that partially addresses it and who uses it.
3. Say what placement control you give up, and which systems therefore do not use it.
4. Say what happens to range queries.

### The alternatives drill

1. Describe rendezvous hashing in two sentences.
2. Give its cost and say at what cluster size you would prefer it.
3. Describe jump consistent hash and its restriction.
4. Name the `O(1)` alternative and who built it.

### The failure drill

For each, say what happens and what you would add:

1. Two clients disagree about which nodes are alive.
2. A key hashes past the last node on the ring.
3. A node repeatedly leaves and rejoins.
4. One key receives 40 percent of all traffic.
5. Someone asks for all keys between X and Y.
6. A large tenant must be kept on a specific machine in a specific country.

Two of the six are not solved by consistent hashing at all. Name them and say what is.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Is this a valid BST? Are you sure your check is correct?*
   The invariant with "all the subtree", the wrong answer killed with a counter-example you produce
   yourself, the range formulation with bounds narrowing, the `None`-not-`INT_MIN` detail, the duplicates
   convention, and the inorder alternative offered.

2. *You add a cache node. How many keys move?*
   The `1/(N+1)` number, why modulo is catastrophic with the origin-load arithmetic, the four-step
   mechanism with the node count absent from it, both reasons for virtual nodes, and the honest limits.

3. *Why virtual nodes?*
   Distribution with the 63-percent example, then failure spreading with the doubling-and-cascade
   arithmetic, and the standard count.

---

## Before you move on

- [ ] I can produce the killer input from memory, before being asked.
- [ ] I can say what `search` does on that tree, and why that is worse than a wrong answer.
- [ ] I can write the range version and label a tree with its intervals.
- [ ] I use `None` for unbounded and can give the input that breaks `INT_MIN`.
- [ ] I use `<=` and can say what `<` accepts.
- [ ] I can state the duplicates convention and which comparison it changes.
- [ ] I can write the inorder version with one variable, and the iterative one.
- [ ] I can state the one-or-two-violations rule and which nodes to take.
- [ ] I can write the one-pass largest-BST-subtree and name what it returns.
- [ ] I can say why `hash % N` breaks, in terms of where `N` appears.
- [ ] I can give the movement fractions for modulo and for the ring.
- [ ] I can compute the origin load spike from a naive cache resize.
- [ ] I can state the four steps of the ring mechanism.
- [ ] I can give both reasons for virtual nodes and say which is usually missed.
- [ ] I can do the failure arithmetic for 1 versus 200 virtual nodes.
- [ ] I can name the wrap-around bug and the hash-determinism bug.
- [ ] I can say what consistent hashing does not solve, and what does.
- [ ] I can name one alternative and the cluster size where I would prefer it.
- [ ] I answered all three questions above out loud.
