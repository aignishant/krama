---
day: 98
track: practice
title: "Practice — What a tree is, and the vocabulary you need"
status: written
---

# Day 098 · Practice

**DSA topic:** What a tree is, and the vocabulary you need
**System design topic:** Vertical versus horizontal scaling

---

## Code these, in this order

One rule for the whole set: **say the convention before you write the base case.** Edges or nodes.
Every off-by-one in this topic comes from not deciding that in advance, and it costs four seconds to
decide.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Maximum Depth of Binary Tree | LeetCode 104 (Easy) | The five-line shape, and which convention LeetCode uses. |
| 2 | Count Complete Tree Nodes | LeetCode 222 (Easy) | The same shape with `+` instead of `max` — then the follow-up about doing better. |
| 3 | Minimum Depth of Binary Tree | LeetCode 111 (Easy) | The trap: `min` is wrong when one child is missing. |
| 4 | Binary Tree Level Order Traversal | LeetCode 102 (Medium) | Capturing the queue length before the loop, which is the level boundary. |

### On problem 1, write both conventions

Write it returning `-1` for `None` and again returning `0`. Run both on an empty tree, a single node,
and a chain of three. Record all six answers and say which one LeetCode accepts.

### On problem 2, then answer the follow-up

The naive version is `O(n)`. The problem says the tree is *complete*. Say what that shape guarantees,
and what complexity is achievable because of it. You do not have to write it today — say the idea.

### On problem 3, find the trap before running it

Write `1 + min(left, right)` and run it on a tree where the root has only a right child. Record the
answer, then say why it is wrong, then fix it. This is the single most-failed easy tree problem.

### On problem 4, do not use recursion

Use a queue. Capture `len(queue)` into a variable before the inner loop and say, in one sentence, why
that variable is exactly one level.

---

### The vocabulary drill

Define each in one sentence, then give an example from the wedding tree:

1. root, leaf, parent, child, sibling
2. edge, path, level, subtree
3. ancestor, descendant, degree, internal node, forest
4. Then say which two of the above are properties of a *node* and which is a property of the *tree*.

### The height-and-depth drill

1. Define depth and height, in opposite directions, in one sentence each.
2. Say which one is computed on the way up and which is carried down, and why.
3. For a given tree, state the depth of three nodes and the height of three nodes.
4. Say why a leaf's height is always 0 whatever its depth.
5. Say what "the depth of the tree" should have been.

### The convention drill

1. Give both base cases and what each returns for a single node.
2. Say which one LeetCode 104 expects.
3. Write the sentence you would say to an interviewer to settle it in four seconds.
4. Mix the two inside one function and describe how the bug shows up.

### The shape drill

1. Write the five-line shape that every tree function takes.
2. Write `height`, `count_nodes` and `count_leaves` against it, and say what differs in each.
3. Say what the base case always is, and why it is not defensive coding.
4. Say why `count_leaves` cannot return 1 for `None`, with the input that proves it.

### The two-facts drill

1. State the edge-count fact and prove it in one line.
2. State the one-path fact and say what it lets you leave out of every traversal.
3. Build a structure where a node has two parents, run `count_nodes`, and say what goes wrong.
4. Say what such a structure is called instead.

### The shapes drill

1. Draw full, complete, perfect, balanced and degenerate, each with five to seven nodes.
2. Give the node count of a perfect tree of height `h`.
3. Say which shape lets a tree live in an array, and name the structure that uses it.
4. Say which shape makes a tree behave like a linked list, and how you would build one by accident.

### The cost drill

1. State the time and space of a full tree walk.
2. Give the stack depth for a balanced and a degenerate tree of a million nodes.
3. Say which traversal costs `O(height)` and which costs `O(width)`, and what the widest level of a
   perfect tree holds.
4. Explain why `is_balanced` as written is `O(n²)` and say what the fix is called.
5. Give the height of a perfect tree for n = 1,000, a million and a billion.

### The break-it drill

Trigger each and record the exact output or error:

1. `height` with no `None` check.
2. `count_leaves` returning 1 for `None`.
3. A recursive walk on a chain of 10,000 nodes.
4. Two subtrees sharing one node, then counting.
5. `min(left, right)` for minimum depth on a one-sided tree.

---

### The two-directions drill

1. Define both directions in one sentence each.
2. Give three things vertical scaling buys and three it costs.
3. Give three things horizontal scaling buys and three it demands.
4. State the one-sentence rule for choosing.

### The first-question drill

1. Say the question you ask before anything else, and why.
2. Give an example where horizontal scaling helps nothing at all.
3. State the sentence about throughput and latency.
4. Say what you would do instead for the case where it helps nothing.

### The knee drill

1. Reproduce the price-per-vCPU table and say where it stops being flat.
2. State the three stopping conditions for vertical scaling.
3. Say which of the three is a fact rather than a judgement.
4. Give the practical top-end RAM figure and say what it implies for most companies' databases.

### The availability drill

Compute each, showing the working:

1. Downtime per year at 99%, 99.9%, 99.99%.
2. Combined availability of two independent machines at 99.9%, either of which can serve.
3. The improvement factor from adding that second machine.
4. Say what assumption the calculation makes, and three ways real deployments break it.

### The per-tier drill

For each tier, say vertical or horizontal and give the reason:

1. Stateless application servers.
2. The cache.
3. The primary database.
4. Read replicas.
5. Media files.

Then say why "vertical or horizontal" is the wrong shape of question at the system level.

### The database drill

1. Name the two stages of scaling a database horizontally, in order.
2. Say what each one scales and what each one costs.
3. Say what sharding takes away permanently.
4. Give the sizing comparison for a database at 4,000 writes/second on 8 vCPU, both ways.
5. Say what you would do first regardless of the capacity answer, and why.

### The fifty-servers drill

Name the three things that break when going from one app server to fifty, in the order you meet them,
and say what each one's fix is. Then say why none of them is a reason not to scale out.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *What is the height of this tree? What is the depth of that node?*
   Both defined in opposite directions, the convention declared in advance, the up-versus-down asymmetry
   named, the numbers given, and the cost stated with the degenerate-tree caveat.

2. *Your database is at capacity. Bigger box, or more boxes?*
   The first question about slow-versus-many, vertical first with the three stopping conditions, the
   availability number that no bigger box can buy, what sharding costs permanently, and the standby
   replica you would add regardless.

3. *What makes something a tree rather than a graph?*
   One parent each and no cycles, therefore exactly one path from the root, therefore no visited set and
   therefore natural recursion — plus the `n − 1` edges fact with its one-line proof.

---

## Before you move on

- [ ] I can define all fifteen vocabulary terms without hesitating.
- [ ] I can define depth and height in opposite directions and say which is which.
- [ ] I know which one is computed upward and which is passed downward.
- [ ] I say the convention out loud before writing a base case.
- [ ] I can write the five-line shape that every tree function takes.
- [ ] I can write `height`, `count_nodes` and `count_leaves` and say what differs.
- [ ] I can prove the `n − 1` edges fact in one line.
- [ ] I can say what the one-path property lets me leave out of every traversal.
- [ ] I can draw all five named shapes.
- [ ] I know which shape lets a tree live in an array.
- [ ] I can state the stack depth for balanced and degenerate trees of a million nodes.
- [ ] I know why `is_balanced` as written is `O(n²)`.
- [ ] I never assume a binary tree is balanced or a search tree.
- [ ] I can state the first question to ask before choosing a scaling direction.
- [ ] I can say the sentence about throughput and latency.
- [ ] I can give the three stopping conditions for vertical scaling.
- [ ] I can compute the availability of one machine versus two and give the factor.
- [ ] I can assign a direction to each of the five tiers with a reason.
- [ ] I can say what sharding costs permanently, and why it is not a migration cost.
- [ ] I answered all three questions above out loud.
