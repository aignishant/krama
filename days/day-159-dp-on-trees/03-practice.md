---
day: 159
track: practice
title: "Practice — DP on trees"
status: written
---

# Day 159 · Practice

**DSA topic:** DP on trees
**System design topic:** Design Netflix

---

## Code these, in this order

One rule for the whole set: **before writing the function, say two sentences out loud — what I record, and
what I return.** If they are the same thing, say so explicitly. If they differ, the bug lives in the gap
between them, and naming it in advance is the only reliable defence.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Diameter of Binary Tree | LeetCode 543 (Easy) | Record versus return, in its clearest form. |
| 2 | Binary Tree Maximum Path Sum | LeetCode 124 (Hard) | The same, plus the clamp and the `-inf` base. |
| 3 | House Robber III | LeetCode 337 (Medium) | The `(take, skip)` state, and why one number fails. |
| 4 | Longest Univalue Path | LeetCode 687 (Medium) | Record/return again, with a condition on the edge. |
| 5 | Sum of Distances in Tree | LeetCode 834 (Hard) | Rerooting, and why the naive version is `O(n²)`. |
| 6 | Binary Tree Cameras | LeetCode 968 (Hard) | Three states per node, and a greedy that also works. |

### On problem 1, return the recorded value

Write `return left + right + 1` instead of `1 + max(left, right)`. Run it on a balanced seven-node tree and
record what comes back. **Say what that number actually is**, and why it looks plausible as a diameter.

### On problem 2, remove the clamp

Drop the `max(0, ...)`. Run on a node with value 2 and two children of −5 and −3. Record the answer against
the correct one. **Say what the path was forced to do.**

### On problem 2, start `best` at zero

Run on a tree where every value is negative. Record what you get and what the answer should be. **Say what
path the zero corresponds to**, and why that path is not allowed.

### On problem 3, return one number

Return `max(take, skip)` instead of the pair. Construct a small tree where the answer comes out too large, and
**write down the illegal selection it corresponds to** — which nodes it invited together.

### On problem 5, write the naive version and time it

Run a full traversal from every node. Time it at `n = 2,000` and `n = 10,000`. **Extrapolate to 30,000** and
say whether it would pass. Then write the two-pass version and time that.

### On problem 5, derive the rerooting line

Before coding pass two, write out in words what happens to the distance sum when the root moves across one
edge from `u` to its child `v`. **Count how many nodes get closer and how many get further.** Then write the
line.

### Then the depth drill

Build a tree of 2,000 nodes in a straight line. Run your recursive solution and record the exact error. Then
set `sys.setrecursionlimit(200000)` and run it on a 150,000-node line. **Record what happens.** Then write the
iterative version and run it on the same input.

### Then the post-order-from-a-stack drill

Write the explicit-stack version of problem 1 from memory. **Say what the boolean flag is for**, in one
sentence, and what you get without it.

---

### The pattern drill

1. Write the four-line skeleton from memory.
2. Say why post-order is the right traversal.
3. Say what tree DP gets for free that interval DP does not.
4. Give the time and space, and what the space depends on.

### The record-versus-return drill

1. State the two sentences for diameter.
2. Say why the parent cannot use the recorded value.
3. Say what returning the wrong one produces, and whether it errors.
4. Give the test that decides whether a problem needs an outer variable.
5. Name three problems where the answer can live anywhere.

### The state drill

1. Say why house robber on a tree needs two numbers.
2. Give both transitions.
3. Say what a single number loses, and what illegal thing it permits.
4. Say which earlier topic this is the same idea as.

### The negatives drill

1. Say what the clamp does and where it goes.
2. Give an example where omitting it is wrong.
3. Say why `best` starts at `-inf`.
4. Say what a `best` of 0 would correspond to.

### The rerooting drill

1. Say what question needs it.
2. Give the naive cost and the constraint that rules it out.
3. Describe pass one and what each array holds.
4. Give the pass-two line and derive it in words.
5. Say what the total cost is.

### The depth drill

1. Give Python's default limit and what a line-shaped tree does.
2. Say why a line-shaped tree is a realistic input.
3. Say what `setrecursionlimit` fixes and what it does not.
4. Describe the explicit-stack post-order pattern.
5. Say when you would bother, and when you would not.

### The break-it drill

Trigger each and record the exact output or error:

1. Returning `left + right` from a depth function.
2. No clamp on negative children.
3. `best = 0` in max path sum.
4. One number instead of `(take, skip)`.
5. A 2,000-node line, recursively.
6. `setrecursionlimit(200000)` on a 150,000-node line.
7. A traversal on a bidirectional adjacency list with no `parent` guard.

Four of the seven give no error at all. Name them.

---

### The comparison drill

1. Give the six-row comparison with a user-generated video platform.
2. Say what the single driving fact is.
3. Compute the catalogue size and compare it with a year of YouTube uploads.

### The delivery drill

1. Say what reactive caching does at a midnight release, with numbers.
2. Describe predictive pre-positioning and when the transfer happens.
3. Say why both sides agree to an ISP-embedded box.
4. Give the cost comparison, bought against built.
5. Say what makes building it possible here and not at YouTube.
6. Say what happens when the demand forecast is wrong, in both directions.

### The encoding drill

1. Say what a fixed ladder gets wrong, in both directions, with an example.
2. Describe per-title and per-shot encoding.
3. Say why a perceptual quality metric is required.
4. Give the compute cost for the whole catalogue and the saving.
5. Say precisely why YouTube cannot make the same trade.

### The playback drill

1. Name the three things this adds to plain adaptive streaming.
2. Say where DRM policy is enforced, and why not at the edge.
3. Say what CMAF with common encryption saves.
4. Say why entitlement checks come first.
5. Compute the watch-position write rate and say what absorbs it.

### The home page drill

1. Say why the home page is the product.
2. Describe the row structure and what is ranked.
3. Say what is precomputed and what is real-time.
4. Say why real-time ranking is not viable, with numbers.
5. Say what a new user sees, and why that matters.

### The scale drill

1. Compute daily egress and peak bits per second.
2. Give the appliance count and amortised cost.
3. Say which spike is a control-plane problem rather than a bandwidth one.
4. Say what fraction of the company's spend infrastructure is, and what follows.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the diameter of a binary tree.*
   The post-order pattern, the two sentences about record and return, why the parent cannot use the recorded
   value, the complexity, and what happens on a line-shaped tree.

2. *House robber, but on a tree.*
   The two-number state, both transitions, exactly what one number loses, and what illegal answer it
   produces.

3. *Design Netflix — and how is it different from YouTube?*
   The catalogue fact, predictive pre-positioning, Open Connect and why both sides agree, per-title encoding
   with its amortisation argument, and the precomputed home page.

---

## Before you move on

- [ ] I can write the post-order tree DP skeleton from memory.
- [ ] I know the recursion is the fill order, and why.
- [ ] I say what I record and what I return, before writing.
- [ ] I know why the parent cannot use the recorded value.
- [ ] I know returning the wrong one gives no error.
- [ ] I have the test for whether a problem needs an outer variable.
- [ ] I know the clamp and where it goes.
- [ ] I know `best` starts at `-inf` and what 0 would mean.
- [ ] I can give the `(take, skip)` state and both transitions.
- [ ] I can say what one number loses, and the illegal selection it allows.
- [ ] I know this is the same idea as the stock problem's mode.
- [ ] I know the time and space, and what the space depends on.
- [ ] I know Python's recursion limit and what a line-shaped tree does.
- [ ] I know `setrecursionlimit` can segfault rather than raise.
- [ ] I can write the explicit-stack post-order version.
- [ ] I know what the boolean flag is for.
- [ ] I know rerooting is `O(n)` where the naive version is `O(n²)`.
- [ ] I can derive the pass-two line in words.
- [ ] I know a bidirectional adjacency list needs a `parent` guard.
- [ ] I can give the six-row Netflix/YouTube comparison.
- [ ] I know the catalogue size and why it drives everything.
- [ ] I can explain predictive pre-positioning and its timing.
- [ ] I know why ISPs agree to host an appliance.
- [ ] I can give the bought-versus-built cost comparison.
- [ ] I know what makes building it possible here and not at YouTube.
- [ ] I can explain per-title encoding and the amortisation argument.
- [ ] I know why a perceptual metric is required.
- [ ] I can name the three additions to plain adaptive streaming.
- [ ] I can compute the watch-position write rate.
- [ ] I know the release spike is a control-plane problem.
- [ ] I answered all three questions above out loud.
