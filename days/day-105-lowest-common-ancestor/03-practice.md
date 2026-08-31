---
day: 105
track: practice
title: "Practice — Lowest common ancestor"
status: written
---

# Day 105 · Practice

**DSA topic:** Lowest common ancestor
**System design topic:** Read replicas and replication lag

---

## Code these, in this order

One rule for the whole set: **ask the two questions before writing** — plain tree or search tree, and are
both nodes guaranteed to be present. They change the code, and asking takes ten seconds.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | LCA of a Binary Search Tree | LeetCode 235 (Medium) | Noticing that the ordering removes the search entirely. |
| 2 | LCA of a Binary Tree | LeetCode 236 (Medium) | The overloaded return value, and recursing both sides. |
| 3 | LCA of a Binary Tree II | LeetCode 1644 (Medium) | What breaks when the nodes may be absent. |
| 4 | LCA of Deepest Leaves | LeetCode 1123 (Medium) | The same postorder shape returning a pair. |

### On problem 1, write it iteratively

No recursion. Then say the time and space, and compare both against the general version on a balanced
million-node tree.

### On problem 2, say the three meanings before you code

Write the three meanings of the return value down first. Then write the six lines. If the code comes
before the sentence, you are recalling rather than deriving.

### On problem 3, break problem 2 first

Take your working solution from problem 2 and call it with a node that is not in the tree. Record what it
returns. Then fix it, and say why the count must happen after recursing.

### On problem 4, notice the shape

Compare it with day 102's diameter and day 104's max path sum. Say what all three share, and what the
return value carries in each.

---

### The two-questions drill

1. State both questions and say what each one changes.
2. Say what the standard solution returns when a node is absent.
3. Say what changes if it is a BST.
4. Say what changes if nodes carry parent pointers.

### The definition drill

1. Define LCA in one sentence.
2. Say why the root is almost never the answer.
3. State the self-ancestor rule and give an example where it decides the answer.
4. Say what happens to the algorithm if you omit that case.

### The three-meanings drill

1. Write the six lines from memory.
2. State the three meanings of the return value.
3. Say what `left and right` means in words.
4. Say what `left or right` is doing, and to whom.
5. Say why both recursive calls must always run.

### The assumption drill

1. Construct a tree and a call where the plain solution is wrong.
2. Say why it stops early, and why that is correct under the guarantee.
3. Write the counting version.
4. Say why the count must come after the recursion, with the input that proves it.
5. Name a version of the solution that handles absence for free.

### The BST drill

1. Write the iterative version from memory.
2. Say what the `else` branch covers — all three cases.
3. Change `<` to `<=` and find the input it breaks.
4. Run the BST version on a non-BST and say what happens and why there is no error.
5. Give both complexities against the general version, with numbers at n = 1,000,000.

### The parent-pointer drill

1. Name the three methods and their costs.
2. Write the two-pointer swap.
3. Say why both pointers travel the same total distance.
4. Name the linked-list problem this is the same as.

### The many-queries drill

1. Compute the cost of 100,000 naive queries on a 100,000-node tree.
2. Name three preprocessing approaches and their build and query costs.
3. Say which one you would name first and what it stores.
4. Say the one-sentence rule for when to switch from walking to preprocessing.

### The break-it drill

Trigger each and record the exact output:

1. Comparing `.val` instead of using `is`, on a tree with duplicate values.
2. Short-circuiting after the left recursive call.
3. Omitting the `node is p or node is q` case.
4. The BST version on a non-BST.
5. `<=` in the BST comparison, where `p` is the current node.
6. The plain solution with an absent node.
7. A recursive LCA on a 10,000-node chain.

---

### The mechanism drill

1. Say what a read replica is and what still goes to the leader.
2. Give typical read:write ratios for four kinds of product.
3. Compute the leader's load before and after adding three replicas at 6,000 reads and 120 writes.
4. Say which kind of product replicas do not help.

### The lag drill

1. Give typical lag figures for four situations.
2. Say why the average is the wrong number to quote.
3. Name five causes of lag.
4. Describe the feedback loop between read traffic and lag.

### The three-guarantees drill

1. Name all three guarantees users expect and give the everyday phrasing of each.
2. Say which one produces support tickets and why.
3. Say which one looks like data loss.
4. Say which one is mostly a sharding problem.

### The fixes drill

1. Name the four fixes for read-your-own-writes in order.
2. For each, say its precision and its cost.
3. Compute the share of read load that returns to the leader under the default fix.
4. Say which fix real systems expose as a per-request option, and name two.
5. Say which one is not a fix, and why you would mention it anyway.

### The monotonic drill

1. Describe the failure in two sentences.
2. Say why it is worse than plain staleness.
3. Give the fix and the two costs it carries.
4. Say what happens to pinned users when their replica dies.

### The ceiling drill

1. State the sentence about every replica applying every write.
2. Fill in the table of write rate against replica capacity left for reads.
3. Say what the answer is once the ceiling is reached.
4. Say what you would try before that, in order.

### The operations drill

1. Name the lag metric for two databases.
2. Describe the heartbeat method and say what it catches that the metric misses.
3. Give the three alert thresholds and the action at each.
4. Say why automatic eviction matters, in terms of what the failure looks like.
5. Name four jobs a replica can have besides serving reads.

### The failure drill

For each, say what happens and what you would add:

1. A user writes and reads 50 ms later.
2. Two consecutive reads land on replicas with different lag.
3. A twenty-minute report runs on a serving replica.
4. A replica is four minutes behind and still in the read pool.
5. The write rate reaches the machine's ceiling.
6. A leader fails over to a replica that was behind.

Two of the six are the same underlying number wearing different names. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the lowest common ancestor of these two nodes.*
   The two questions asked first, the definition with the self-ancestor rule, the algorithm described as a
   question asked of each subtree, the three meanings of the return value, why the early return is correct
   under the guarantee, and then the BST version with the reason it is different.

2. *The user posted a comment and cannot see it. What happened?*
   The failure named precisely, "nothing is broken" said explicitly, the timing that makes it likely rather
   than rare, the default fix with its cost as a percentage, the sharper alternatives, and the monotonic
   sibling failure.

3. *Why is your BST answer different from your binary tree answer?*
   Search versus map, the walk-down rule, `O(height)` and `O(1)` against `O(n)` and `O(height)`, and the
   numbers at a million nodes.

---

## Before you move on

- [ ] I ask both questions before writing any LCA code.
- [ ] I can state the three meanings of the return value.
- [ ] I can write the six lines from memory and explain each.
- [ ] I know why both recursive calls must run.
- [ ] I can construct the input where the standard solution is wrong.
- [ ] I know why the count must come after the recursion.
- [ ] I can write the BST version iteratively and say what the `else` covers.
- [ ] I know what happens when the BST version meets a non-BST.
- [ ] I can give both complexities with numbers at a million nodes.
- [ ] I can write the parent-pointer two-pointer swap and name the problem it matches.
- [ ] I can name three preprocessing approaches for many queries.
- [ ] I can name the failure when a user cannot see their own write.
- [ ] I can say "nothing is broken" and explain why both operations were correct.
- [ ] I can name all four fixes with their precision and cost.
- [ ] I can compute the read load that returns to the leader under the default fix.
- [ ] I can describe monotonic reads and say why it looks like data loss.
- [ ] I can state the every-replica-applies-every-write ceiling with the table.
- [ ] I know how to measure lag honestly and what to do when it exceeds a threshold.
- [ ] I answered all three questions above out loud.
