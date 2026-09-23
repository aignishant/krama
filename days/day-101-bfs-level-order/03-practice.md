---
day: 101
track: practice
title: "Practice — Breadth-first traversal: level order"
status: written
---

# Day 101 · Practice

**DSA topic:** Breadth-first traversal: level order
**System design topic:** Caching: the single biggest win

---

## Code these, in this order

One rule for the whole set: **say the invariant out loud before writing the loop** — *at the top of the
outer loop, the queue holds exactly one complete level.* Everything else in these four problems is one
differing line.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Binary Tree Level Order Traversal | LeetCode 102 (Medium) | Capturing `len(queue)` before draining. |
| 2 | Binary Tree Right Side View | LeetCode 199 (Medium) | The same loop; the last node of each level. |
| 3 | Minimum Depth of Binary Tree | LeetCode 111 (Easy) | Where BFS is genuinely faster, and the `min` trap. |
| 4 | Binary Tree Zigzag Level Order Traversal | LeetCode 103 (Medium) | Reversing the list, not the traversal. |

### On problem 1, break the boundary on purpose

Replace the inner `for _ in range(level_size)` with `while queue`. Run it and record the output. Say in
one sentence why the first level turned out to be the whole tree.

### On problem 2, do it two ways

Once with BFS taking the last of each level, once with a DFS that visits right before left and records
the first node seen at each depth. Say which one you would write and why the DFS version needs no queue.

### On problem 3, write the wrong recursion first

Write `1 + min(left, right)`, run it on a root with only a right child, and record the answer. Then say
what "leaf" actually means and fix it. Then write the BFS version and say what it costs on a tree whose
left branch is 10,000 deep.

### On problem 4, try the wrong approach for two minutes only

Attempt to alternate the queue's direction. Stop after two minutes, then do it with `level[::-1]`. The
point of the exercise is to feel how much cheaper the right approach is.

---

### The one-swap drill

1. Write iterative preorder from yesterday.
2. Change two things to make it level order, and name them.
3. Say why a stack goes deep and a queue goes wide.
4. Say what the output is missing without the level boundary.

### The invariant drill

1. State the invariant in one sentence.
2. Write the outer and inner loops from memory.
3. Say what `level_size` is, and why it must be captured before any append.
4. Trace the queue at the top of every outer iteration for a six-node tree.

### The three-ways drill

1. Write the `level_size` version.
2. Describe the sentinel version and name its edge case.
3. Write the DFS-with-depth version.
4. Say what each one costs in space, and when you would pick the third.

### The variants drill

Write each as one differing line on the same skeleton:

1. Level order. 2. Right side view. 3. Level averages. 4. Level maximums. 5. Zigzag.
6. Maximum width.

Then say why memorising the skeleton beats memorising six problems.

### The when-BFS drill

1. Name the three families of problems that want BFS.
2. Name the family that wants DFS instead, and say why BFS cannot do it.
3. Construct the tree that makes minimum depth much faster with BFS, and count nodes visited both ways.
4. Say what BFS on an unweighted graph guarantees.

### The space drill

1. State the space of BFS and of DFS in terms of the tree's shape.
2. Compute both for a perfect million-node tree.
3. Compute both for a ten-thousand-node chain.
4. Say which one raises `RecursionError` and on which shape.
5. Say why `O(n)` is a worse answer than `O(width)`.

### The deque drill

1. Say what `list.pop(0)` costs and why.
2. Compute the element moves for a level-order traversal of 100,000 nodes with a list.
3. Say what error you get when the list version is too slow.
4. Write the first line of every BFS you will ever write.

### The break-it drill

Trigger each and record the exact output or error:

1. `while queue` as the inner loop.
2. Appending `None` children.
3. No empty-tree guard.
4. A list with `pop(0)` on a large tree, timed.
5. `1 + min(left, right)` on a one-sided tree.
6. Trying to compute subtree sums with a level-order loop — say why you cannot.

---

### The why-it-works drill

1. Name the two facts that make caching work.
2. Give the latency figures for the four layers.
3. State the access-pattern assumption and say what happens to caching without it.
4. Give the top-1% and top-10% request shares.

### The arithmetic drill

Compute each, showing the working:

1. Effective latency at hit rates of 0, 50, 90, 95 and 99 percent, with a 0.5 ms cache and a 20 ms origin.
2. Database load at 6,000 read QPS for the same five hit rates.
3. Say what shape the latency curve has and why the last few percent matter.
4. Cache size for a 90 percent hit rate on 10M profiles of 2 KB each.
5. Refreshes per day per key for TTLs of 10 s, 60 s, 5 min and 1 day.

### The four-layers drill

1. Name all four layers and what each one saves.
2. Say which is usually the biggest win for a media-heavy product.
3. Say which one is free and what "configuring it" means.
4. Give the two sub-choices inside the application layer and when to use each.

### The patterns drill

1. Write the cache-aside read path in five lines.
2. Say what cache-aside gives you that read-through does not, in one sentence about failure.
3. Name the three write patterns and give a use case for each.
4. Say which write pattern can lose data, and what kind of data that is acceptable for.

### The key-design drill

1. Give the three rules for cache keys.
2. Write keys for: a user's profile, page 3 of a user's feed, a product price in two currencies.
3. Give an example of a key that will never hit.
4. Say why namespacing matters.

### The stampede drill

1. Describe the stampede in two sentences.
2. Compute the burst for 1,000 in-flight requests on one expiring key.
3. Name three fixes and say which two you would use by default.
4. Say what jitter is preventing, with the thousand-keys example.

### The what-not-to-cache drill

1. State the rule about slow versus wrong.
2. Give three values you would never cache for a decision.
3. Say what "cache the display, not the decision" means with an example.
4. Name three data shapes where a cache adds work rather than removing it.

### The failure drill

For each, say what happens and what you would add:

1. Redis goes down.
2. Redis restarts empty during peak traffic.
3. A wrong value is written into the cache.
4. A user edits their profile and immediately reloads the page.
5. Every request has a different cache key.
6. The hit rate is 99 percent on data that changes every second.

Two of the six are not availability problems. Name them and say what they are.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Print the tree level by level. Now print each level as its own list.*
   The one swap from a stack to a queue, the invariant stated before the code, `level_size` with the
   reason it is correctness rather than optimisation, `deque` with the `O(n²)` warning, and `O(width)`
   space with both extremes.

2. *Where would you put a cache in this system?*
   All four layers named before choosing, the read:write ratio as the justification, a hit rate with the
   unevenness assumption stated, the load arithmetic, the TTL framed as a staleness decision, and the
   stampede pre-empted.

3. *A very popular item's cache entry expires. What happens?*
   The stampede described with the burst arithmetic, per-key locking and jittered TTLs as the fixes, and
   refresh-ahead as the optional third.

---

## Before you move on

- [ ] I can turn iterative preorder into level order by changing two things.
- [ ] I can state the queue invariant in one sentence.
- [ ] I can write the `level_size` loop from memory and say why the capture is correctness.
- [ ] I ran the version without the capture and can explain the output.
- [ ] I can write five variants as one differing line each.
- [ ] I can name the three families that want BFS and the one that wants DFS.
- [ ] I can construct the tree where BFS is genuinely faster for minimum depth.
- [ ] I know the `1 + min(left, right)` trap and what "leaf" really means.
- [ ] I can state BFS space as `O(width)` and give both extremes.
- [ ] I always write `from collections import deque` first.
- [ ] I can name the two facts that make caching work.
- [ ] I can name all four cache layers and what each saves.
- [ ] I can compute effective latency and database load for any hit rate.
- [ ] I can size a cache from the data size and a target hit rate.
- [ ] I can write cache-aside and say what it gives me on failure.
- [ ] I can name the three write patterns and which one loses data.
- [ ] I can describe the stampede with numbers and name two fixes.
- [ ] I can state the slow-versus-wrong rule and give something I would never cache.
- [ ] I answered all three questions above out loud.
