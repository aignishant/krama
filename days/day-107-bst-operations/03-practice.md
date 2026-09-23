---
day: 107
track: practice
title: "Practice — BST insert, search, and delete"
status: written
---

# Day 107 · Practice

**DSA topic:** BST insert, search, and delete
**System design topic:** Sharding, part two: rebalancing and hot spots

---

## Code these, in this order

One rule for the whole set: **write `node.left = f(node.left, ...)` as a unit.** Every structural change
in this lesson is the recursive call being reattached. Forgetting the assignment computes the right
answer and throws it away, with no error.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Insert into a Binary Search Tree | LeetCode 701 (Medium) | The reattachment idiom, and that a new value is always a leaf. |
| 2 | Delete Node in a BST | LeetCode 450 (Medium) | The three cases, and deriving the successor rather than reciting it. |
| 3 | Inorder Successor in BST | LeetCode 285 (Medium) | The two cases, and finding the last left turn on the way down. |
| 4 | Trim a Binary Search Tree | LeetCode 669 (Medium) | The same reattachment idiom, used for something else. |

### On problem 1, then break it

Remove the assignment — call `insert(node.left, value)` without storing the result — and run it. Record
what the tree looks like afterwards and say why nothing raised.

### On problem 2, delete the root first

Test with a two-child root before anything else. Then run the same code with a `delete` that returns
`None` instead of the new subtree root, and say what happens to the root.

### On problem 3, do both cases

Write the version that uses the right subtree's minimum, and the version that finds the last left turn.
Say which case each one handles and why you need both.

### On problem 4, notice the shape

Compare it line by line with `delete`. Say what is the same and what differs, and what that tells you
about the idiom.

---

### The idiom drill

1. Write the reattachment frame for `delete` from memory, before any cases.
2. Say what the assignment is doing that a parent pointer would otherwise do.
3. Say why the function must return a node rather than nothing.
4. Say why `root = delete(root, key)` is required at the top level.

### The three-cases drill

1. Name the three cases and what each returns.
2. Write the first two as two lines and say why that covers three situations.
3. Draw all three on a seven-node tree.
4. Say which one is the only interesting one and why.

### The successor drill

1. State the constraint on whatever fills the gap, in one sentence.
2. Say how many values in the whole tree satisfy it, and which they are.
3. Give a wrong replacement and show the resulting inorder sequence.
4. Say why the successor has no left child.
5. Say why the inner delete cannot recurse more than one level.

### The predecessor drill

1. Write the predecessor version.
2. Delete the same node with both and compare the resulting roots.
3. Confirm the inorder sequences match.
4. Say what always using one side does over many deletions, and what real implementations do.

### The iterative drill

1. Write `delete` iteratively.
2. Say what extra bookkeeping it needs and why.
3. Say how it handles deleting the root.
4. Say what this tells you about what the recursive version's assignment was doing.

### The lazy-deletion drill

1. Write a node with a `deleted` flag and the three methods.
2. Say what it costs and what it buys.
3. State the standard rebuild threshold.
4. Compute the memory for a million live nodes with a million tombstones.
5. Name the earlier day this idea came from.

### The break-it drill

Trigger each and record the exact output:

1. `delete(node.left, key)` without the assignment.
2. A `delete` that returns `None`, used to delete the root.
3. Replacing with `maximum(node.right)` instead of the minimum — print the inorder result.
4. `minimum(root.right)` instead of `minimum(node.right)`.
5. A recursive delete on a 10,000-node chain.

### The cost drill

1. State the complexity of all three operations and say where delete's extra walk goes.
2. Give the step counts for a balanced and a degenerate million-node tree.
3. Compare deletion against a sorted array at n = 1,000,000.
4. State the space for the recursive and iterative versions.

---

### The modulo drill

1. Compute where key 4117 lives under `% 4` and under `% 5`.
2. State the fraction of keys that move going from N to N+1 under plain modulo.
3. Compute the data moved for 1 TB going from 8 machines to 9, both ways.
4. Say why plain modulo also has no safe intermediate state.

### The indirection drill

1. Describe the logical-shard scheme in two sentences.
2. Say what never changes and what does.
3. Say what the logical shard count is a ceiling on.
4. Say why it should be a power of two.
5. Name three real systems that do this, and Redis's specific number.

### The migration drill

1. Name the four phases in order.
2. For each, say what is happening to reads and to writes.
3. Say which phases are reversible.
4. Describe the race between backfill and dual writes, and two fixes.
5. Say why the backfill is deliberately rate-limited.
6. Give the eight steps for moving a single logical shard, and say which one pauses writes.

### The hot-spot drill

1. Name the four causes.
2. For each, give the evidence that identifies it and the fix.
3. Say which one you check first and why.
4. Say which metric most teams lack, and what it changes.
5. Compute the cluster ceiling when one of four shards takes 60 percent.

### The hot-key drill

1. Name the four remedies in order of cost.
2. Say which one solves a read-heavy hot key completely, and why.
3. Describe key salting and say what it costs.
4. Say when salting is the only option.
5. Compute the effect of caching a key that is 3,500 of a shard's 6,000 req/s at a 95% hit rate.

### The unbounded-key drill

1. Say why a single hot key cannot be split.
2. Give two examples of keys that can grow without limit.
3. Write the composite-key fix for each.
4. Say why this is a design-time rule and not a fix.

### The failure drill

For each, say what happens and what you would add:

1. A client caches a stale shard map during a move.
2. The backfill runs at full speed during peak traffic.
3. Verification is shortened to one day because of a deadline.
4. The logical shard count was set to 16 and you now need 20 machines.
5. A big-bang cutover is done at 2 a.m. and something is wrong at 2:05.
6. One conversation reaches forty million messages.

Two of the six cannot be fixed by changing configuration. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Delete this node from the BST. It has two children.*
   The three cases named first, the reattachment idiom stated as the mechanism, the successor **derived**
   from the constraint rather than asserted, why the inner delete terminates, and the complexity with the
   balance caveat.

2. *One shard is taking 60 percent of the traffic. Now what?*
   Diagnose before prescribing, the four causes with their evidence and fixes, the per-key metric named as
   the thing that decides it, the cluster-ceiling arithmetic, and then the four migration phases if the key
   itself is wrong.

3. *You need to add a shard. How much data moves?*
   Plain modulo's 89 percent, the logical-shard indirection with what changes and what does not, the
   1/(N+1) result, and the ceiling that the shard count imposes.

---

## Before you move on

- [ ] I write `node.left = delete(node.left, key)` as one unit, automatically.
- [ ] I know what happens if the assignment is missing, and that nothing raises.
- [ ] I can name the three cases and write the first two as two lines.
- [ ] I can derive why only the inorder neighbours can fill the gap.
- [ ] I can show the broken inorder sequence from a wrong replacement.
- [ ] I can say why the successor has no left child, unprompted.
- [ ] I can write the predecessor version and say what always using one side does.
- [ ] I can write the iterative version and say what extra bookkeeping it needs.
- [ ] I can describe lazy deletion and its rebuild threshold.
- [ ] I can state all three complexities and the sorted-array comparison.
- [ ] I can compute how much data plain modulo moves at 8 → 9 machines.
- [ ] I can describe the logical-shard indirection and what never changes.
- [ ] I know the shard count is a permanent ceiling, and Redis's number.
- [ ] I can name the four migration phases and which are reversible.
- [ ] I can describe the backfill-versus-dual-write race and two fixes.
- [ ] I can name the four hot-spot causes with evidence and fixes.
- [ ] I know which metric decides the diagnosis, and can compute the cluster ceiling.
- [ ] I can explain why an unbounded key has no after-the-fact fix.
- [ ] I answered all three questions above out loud.
