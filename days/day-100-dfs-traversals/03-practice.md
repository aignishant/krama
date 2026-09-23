---
day: 100
track: practice
title: "Practice — Depth-first traversal: preorder, inorder, postorder"
status: written
---

# Day 100 · Practice

**DSA topic:** Depth-first traversal: preorder, inorder, postorder
**System design topic:** Stateless services and why they scale

---

## Code these, in this order

One rule for the whole set: **do not write three functions.** Write the skeleton — handle `None`,
recurse left, recurse right — and then decide which of the three lines the visit goes on, by asking who
needs what. Then do each one iteratively.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Binary Tree Preorder Traversal | LeetCode 144 (Easy) | The iterative version, and pushing right before left. |
| 2 | Binary Tree Inorder Traversal | LeetCode 94 (Easy) | The go-left loop shape, and `while stack or node`. |
| 3 | Binary Tree Postorder Traversal | LeetCode 145 (Easy) | The reversal trick, then the honest version. |
| 4 | Kth Smallest Element in a BST | LeetCode 230 (Medium) | Why inorder is the answer, and why iterative beats recursive here. |

### On all three of 1 to 3, do the recursion first and time yourself

Each should take under a minute. If any takes longer, you are recalling rather than deriving — write the
skeleton and move the line.

### On problem 1, get the push order wrong on purpose

Push left before right, run it on `[1,2,3]`, and record the output. Say why it looks plausible.

### On problem 2, remove `or node` from the condition

Run it and record the result. Then say why the loop never starts.

### On problem 3, write both versions

The reversal trick first, then the `last_visited` version. For the second, say in one sentence what the
condition `peeked.right is None or last_visited is peeked.right` actually means.

### On problem 4, do it iteratively and say why

Recursive inorder wants to finish the whole tree. Say what the iterative version costs in terms of
`height` and `k`, and why that is better than `O(n)`.

---

### The one-function drill

1. Write the skeleton with the three positions marked.
2. Produce all three orders by moving one line, without looking.
3. State each order as "where the node goes".
4. Say what is identical across all three.

### The choose-the-order drill

For each, say which traversal and why — the reason, not the name:

1. Copy a tree.
2. Compute the height of every node.
3. Print a BST's values in ascending order.
4. Free every node in C++.
5. Record the path from the root to every leaf.
6. Compute the sum of every subtree.
7. Serialise a tree so it can be rebuilt.

Then state the one-line test that decides all seven.

### The by-hand drill

1. Draw a seven-node tree.
2. Draw the anticlockwise loop and mark where each node is passed the first, second and third time.
3. Read off all three orders from the drawing.
4. Check them against code.

### The iterative-preorder drill

1. Write it from memory.
2. Say why right is pushed before left.
3. Run the wrong push order on a three-node tree and record the output.
4. Say what order the wrong version actually produces.

### The iterative-inorder drill

1. Write the five-line shape from memory.
2. Say the shape as one English sentence.
3. Trace it by hand on a four-node tree, recording the stack at every step.
4. Say what `while stack` alone returns, and why.

### The iterative-postorder drill

1. Write the reversal version and say why reversing node-right-left gives postorder.
2. Write the `last_visited` version.
3. Say what the condition means in words.
4. Say which you would write under time pressure and which you would describe.

### The Morris drill

1. Say what it achieves and at what cost.
2. Say what it does to the tree while it runs.
3. Say the two situations in which you could not use it.
4. Say whether you would write it in an interview, and what you would say instead.

### The cost drill

1. State the time for all six implementations.
2. State the space for recursive, iterative and Morris.
3. Give the stack depth for a balanced and a degenerate million-node tree.
4. Compare depth-first against breadth-first on a perfect million-node tree, both directions.
5. Say what constraint bound should make you write the iterative version.

### The break-it drill

Trigger each and record the exact output or error:

1. Left pushed before right in iterative preorder.
2. `while stack` instead of `while stack or node`.
3. A recursive traversal on a chain of 10,000 nodes.
4. `out.append(trail)` instead of `trail[:]` in the paths function.
5. Computing a height in preorder position.
6. Claiming a tree can be rebuilt from its preorder alone — construct two trees with the same preorder.

---

### The definition drill

1. State the definition of stateless in one sentence, using "any instance" and "loses nothing".
2. Say what it does *not* mean.
3. State the one-question test for whether something counts as state.
4. Say how you would verify statelessness experimentally.

### The four-consequences drill

1. Name all four things that break without statelessness.
2. For each, say what a user actually experiences.
3. Say which of the four you live with every day, and which is dramatic but rare.
4. Say why "it scales better" is a worse answer than the list.

### The hidden-state drill

For each, say why it is state and where it should go:

1. Rate-limit counters.
2. Scheduled jobs.
3. A file being uploaded.
4. Sequential id generation.
5. An in-process cache.
6. A WebSocket connection.

Then compute the effective rate limit for 10 servers each enforcing 100 per minute.

### The session-store drill

1. Give the three places a session can live.
2. For each, state the per-request cost and the storage cost.
3. Say what a signed token cannot do, and give two situations where that matters.
4. Compute the daily extra upload for an 800-byte token at 1,000 req/s.
5. State the usual compromise and why it works.

### The stickiness drill

1. Say what sticky sessions are and how they are implemented.
2. Name the four things they cost.
3. Give the typical load spread and the wasted capacity that follows.
4. Compute the fraction of users affected when one of ten servers dies, both ways.
5. State the one-sentence verdict.

### The honest-cost drill

1. Say what you traded away by moving state into a shared store.
2. Say what that store now requires.
3. Give three possible answers to "what happens to a request when it is down".
4. Say why statelessness is fragile against ordinary code changes.

### The stateful-is-right drill

Name four situations where stateful is the correct design, and for each say what makes it acceptable.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Print the tree in inorder. Now do it iteratively.*
   One function with the visit in three places, why inorder matters only for a BST, the recursion, the
   complexity in both parts with the recursion-limit warning, then the go-left shape with the loop
   condition detail called out.

2. *Why should a web server be stateless?*
   The precise definition, the four consequences rather than a slogan, where the session goes with the
   under-one-percent number, sticky sessions pre-empted as a symptom, the state people forget with the
   rate-limiter example, and the honest cost of the shared dependency.

3. *Which traversal would you use, and why?*
   The three-way test — parent acts first, answer comes from the children, BST sorted order — with an
   example of each and the deletion case named.

---

## Before you move on

- [ ] I can produce all three orders by moving one line, from a blank screen.
- [ ] I choose the order by reason and can say the reason, not the name.
- [ ] I can read all three orders off a drawing using the loop trick.
- [ ] I can write iterative preorder and say why right is pushed first.
- [ ] I can write iterative inorder as a shape, including `while stack or node`.
- [ ] I can write postorder by reversal and explain why the reversal works.
- [ ] I can describe the `last_visited` version in words.
- [ ] I can name Morris traversal, its cost, and its catch.
- [ ] I can state time and space for every version, and the depth-versus-width contrast.
- [ ] I know which constraint bound should push me to the iterative version.
- [ ] I know that one traversal never determines the tree, and what two do.
- [ ] I can define stateless precisely and say what it does not mean.
- [ ] I can list all four things that break without it.
- [ ] I can say where the session goes and give the under-one-percent number.
- [ ] I can name four kinds of state people forget, including the rate-limiter bug in numbers.
- [ ] I can give the four costs of sticky sessions and the one-sentence verdict.
- [ ] I can state the honest cost of the shared store and what it requires.
- [ ] I can name four cases where stateful is correct.
- [ ] I answered all three questions above out loud.
