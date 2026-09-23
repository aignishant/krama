---
day: 109
track: practice
title: "Practice — Balanced trees, and why balance matters"
status: written
---

# Day 109 · Practice

**DSA topic:** Balanced trees, and why balance matters
**System design topic:** Back-of-the-envelope estimation

---

## Code these, in this order

One rule for the whole set: **build the degenerate tree first, with your own hands, and measure it.**
Three lines produce it. Every claim in this lesson is about a number you can print.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Balanced Binary Tree | LeetCode 110 (Easy) | Balance at *every* node, in one pass with a sentinel. |
| 2 | Convert Sorted Array to BST | LeetCode 108 (Easy) | The `O(n)` rebuild, and why the middle is the root. |
| 3 | Balance a Binary Search Tree | LeetCode 1382 (Medium) | Flatten to sorted order, then rebuild — the whole cart repacked. |
| 4 | Insert into a Binary Search Tree | LeetCode 701 (Medium) | Then extend it into an AVL insert with the four cases. |

### Before problem 1, build the disaster

Insert 1 to 1,000 in order into a plain BST. Print the height. Then shuffle the same values and do it
again. Record both numbers and the ratio.

### On problem 2, say why the middle

Explain in one sentence why taking the middle element as the root prevents the chain, and give the exact
height it produces.

### On problem 3, then compare against rotations

You have now written the `O(n)` rebuild. Say what a rotation costs instead, and when each is the right
tool.

### On problem 4, extend it

Add height tracking and the four rebalancing cases. Insert 1 to 1,000 in order and print the height. Then
write a treap and do the same, and compare all three heights.

---

### The failing-input drill

1. Write the three lines that produce a degenerate tree.
2. Say why sorted input is the normal case rather than an adversarial one.
3. Give the comparison count for a balanced and a degenerate million-node tree.
4. Say what else fails on a chain besides speed, and quote the error.
5. State the expected height of a randomly built BST.

### The definition drill

1. Define height-balanced, using the word "every".
2. Draw a tree whose root is balanced and which is not balanced.
3. Write the one-pass check with a sentinel and say why `-2` is safe.
4. Say what the naive check costs on a chain.

### The rotation drill

1. Write `rotate_right` in four lines from memory.
2. Write the inorder sequence before and after and say what that proves.
3. Say what happens if the two assignments are swapped.
4. Say what the caller must do with the return value.
5. Say what `O(1)` means here in terms of pointers touched.

### The four-cases drill

1. Name all four cases and the rotations each needs.
2. Draw each one.
3. Say why the zig-zag cases need two rotations, in one sentence.
4. Apply a single rotation to a left-right shape and draw what you get.

### The AVL drill

1. Write `avl_insert` with the four cases.
2. Say in which order the heights must be updated after a rotation, and why.
3. Insert 1 to 1,000 in order and print the height.
4. Compare against the plain BST and the theoretical bound.

### The comparison drill

1. Fill in the AVL versus red-black table from memory.
2. Say which is used by `std::map`, Java and the Linux scheduler, and why.
3. Say which you would pick for a read-heavy in-memory index.
4. Say what you would actually say if asked to implement one.

### The treap drill

1. Write a treap insert from memory.
2. Say what makes it balanced, in one sentence about randomness.
3. Insert 1 to 1,000 in sorted order and print the height.
4. State the guarantee precisely, including the word "expected".
5. Name the other twenty-line option and the product that uses it.

### The B-tree drill

1. Say why databases do not use binary trees.
2. Give the latency figures that make height the cost.
3. Compute the height of a B-tree over a million keys with 500 keys per node.
4. Do the same for a billion rows.
5. Say what decides the number of keys per node.

### The break-it drill

Trigger each and record the exact output or error:

1. A recursive traversal of a 10,000-node chain.
2. A rotation with the two assignments in the wrong order.
3. A rotation whose result is not reattached.
4. Height updates applied in the wrong order after a rotation.
5. A single rotation applied to a left-right shape.
6. The naive balance check on a 2,000-node chain, timed.

---

### The routine drill

1. Name the six steps in order, then the seventh.
2. Say what the seventh step is for, in one sentence.
3. Do all seven for a system with 5 million DAU and 30 actions a day.
4. Say which step is reasoning rather than arithmetic.

### The memory drill

Write from memory, then check:

1. Seconds per day, month and year, with their rounded forms.
2. The three requests-per-day to QPS conversions.
3. The four size conversions.
4. Six typical record sizes.
5. Five machine capacities.
6. Five latency figures.
7. Four standard multipliers.

### The rounding drill

1. State the rule for which direction to round, and why it differs for capacity and savings.
2. Say the sentence you would use out loud when rounding 86,400.
3. Give the error percentage and say why it does not matter.
4. Say what magnitude of error *does* matter, and what catches it.

### The sanity-check drill

1. Name five reference points from memory.
2. Say which one is the counterweight, and what it counterweighs.
3. For each of these, say whether it is plausible and why: 50 TB/day of photos; 200 QPS for a global
   product; 40 servers for a modest site.
4. List the six common errors in order of frequency, with the factor each introduces.

### The worked-example drill

Do each end to end, out loud, under three minutes:

1. A chat application with a billion daily users.
2. A video service — storage and bandwidth.
3. A URL shortener over five years.

For each, say what the *binding constraint* turned out to be, and whether it was the one you expected.

### The consequence drill

From memory, give what each of these means for the design:

1. Peak QPS of 100, 1,000, 10,000, 100,000.
2. Storage of 1 TB, 100 TB, 1 PB.
3. A write rate of 1,000/s, 5,000/s, 10,000/s.

Then say why the third table is the one that ends a discussion.

### The misleading drill

For each, say what the naive estimate misses:

1. A celebrity with fifty million followers posts.
2. A chat app with a million idle users.
3. A system that has been running for four years.
4. A page that loads 1.8 MB of images.
5. An estimate quoted as an average.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *What is the worst case for a BST, and how do real databases avoid it?*
   The sorted input demonstrated rather than described, the fifty-thousand-times number, the good news
   about random insertion, what a rotation is with the inorder property as the justification, AVL against
   red-black, and then B-trees with the disk-read arithmetic.

2. *Estimate the storage for five years of this system's data.*
   The routine announced, every assumption stated as used, actions reasoned rather than guessed, the
   rounding admitted out loud, a sanity check against something known, and then what the number means for
   the design.

3. *Implement a self-balancing tree.*
   Why not red-black, what a treap is in one sentence, why randomness gives balance regardless of insertion
   order, and the "expected not worst case" caveat given honestly.

---

## Before you move on

- [ ] I can produce the degenerate tree in three lines and print its height.
- [ ] I can say why sorted input is normal, not adversarial.
- [ ] I know the expected height of a randomly built BST.
- [ ] I define balanced with the word "every" and can draw the counter-example.
- [ ] I can write `rotate_right` from memory and state the inorder property.
- [ ] I know what happens if the two assignments are swapped.
- [ ] I can name the four cases and say why zig-zags need two rotations.
- [ ] I know in which order heights must be updated after a rotation.
- [ ] I can fill in the AVL versus red-black table and name who uses which.
- [ ] I can write a treap and state its guarantee with the word "expected".
- [ ] I can compute B-tree heights and give the latency figures that justify them.
- [ ] I can recite the six-step routine and the seventh step.
- [ ] I can write the whole memory list without checking.
- [ ] I round out loud with the direction and the reason.
- [ ] I sanity-check every estimate against a named reference point.
- [ ] I can list the six common errors and the factor each introduces.
- [ ] I have done all three worked examples under a timer.
- [ ] I can give the consequence tables from memory.
- [ ] I answered all three questions above out loud.
