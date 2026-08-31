---
day: 110
track: practice
title: "Practice — Building a tree from its traversals"
status: written
---

# Day 110 · Practice

**DSA topic:** Building a tree from its traversals
**System design topic:** Capacity planning: QPS, storage, bandwidth

---

## Code these, in this order

One rule for the whole set: **round-trip every answer.** Build the tree, then traverse it in both orders
and compare against the inputs. Every bug in this lesson produces a valid-looking tree with the values in
the wrong places, and the round trip is the only thing that catches it by eye.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Construct Binary Tree from Preorder and Inorder | LeetCode 105 (Medium) | The split, the position map, and the cursor ordering. |
| 2 | Construct Binary Tree from Inorder and Postorder | LeetCode 106 (Medium) | The mirror: last element, backwards cursor, right subtree first. |
| 3 | Construct BST from Preorder | LeetCode 1008 (Medium) | Why one traversal suffices, and the range walk that avoids sorting. |
| 4 | Construct Binary Tree from Preorder and Postorder | LeetCode 889 (Medium) | Why this is ambiguous in general, and what makes it work here. |

### On problem 1, write the naive version first and time it

Use `inorder.index(...)` and slicing. Time it on a 2,000-node chain against the map-and-indices version.
Record the ratio and say which of the two changes removed which cost.

### On problem 1 again, swap the recursion order

Put `root.right = ...` before `root.left = ...` with the cursor version. Run it on the standard example
and record the tree. Say why nothing raised.

### On problem 2, get the mirror right by reasoning

Do not copy problem 1. Derive it: which element is the root, which way does the cursor move, which subtree
must be built first, and why.

### On problem 4, construct the ambiguity

Before solving it, build the two trees with the same preorder and postorder and print both. Then say what
extra property the problem guarantees that makes the answer unique.

---

### The why-two drill

1. Build the two trees that share a preorder and print all three traversals of each.
2. Say which traversal distinguishes them and which two do not.
3. State what each of the three traversals tells you, in one line each.
4. Say why every working pair contains inorder.

### The split drill

1. Write out the two lists for the standard example and draw the split.
2. Say why the size learned from inorder also cuts the preorder list.
3. Do the split by hand for a seven-node tree, two levels deep.
4. Say what would go wrong if preorder interleaved the two subtrees.

### The complexity drill

1. Name the two separate `O(n²)` costs and where each comes from.
2. Say which change fixes each one.
3. Give the operation counts at n = 2,000 and n = 10,000 for a chain.
4. State the space cost of the fix and say why it is worth it.
5. Say what assumption the position map depends on.

### The cursor drill

1. Write the cursor version from memory.
2. Say why the left recursion must run first.
3. Trace the cursor's value at every call for the standard example.
4. Write the explicit-index version and say the formula for the right subtree's start, in words.

### The mirror drill

1. Write the postorder-plus-inorder version.
2. State the three differences from the preorder version.
3. Say what happens if you build the left subtree first.

### The ambiguity drill

1. State why preorder plus postorder fails, in one sentence about boundaries.
2. Give the two-node counter-example.
3. State the condition under which it does work.
4. Say how the algorithm finds the left subtree's size in that case.

### The BST drill

1. Say why one traversal is enough for a BST.
2. Give the `O(n log n)` approach and the `O(n)` approach.
3. Write the range-based version.
4. Say what it has in common with day 108's validation.

### The break-it drill

Trigger each and record the exact output:

1. The recursion order swapped in the cursor version.
2. `pre_start + left_size` without the `+ 1`.
3. Duplicated values in the inputs.
4. Slicing instead of index ranges, on a 5,000-node chain, timed.
5. Preorder plus postorder on a non-full tree — print both valid answers.
6. A reconstruction of a 10,000-node chain.

---

### The naive-answer drill

1. Do the division for 6,000 peak QPS at 1,000 per server.
2. Say why that number is the answer to a different question.
3. Name all three multipliers and apply them in order.
4. Give the final number and the reasoning for each step.

### The queueing drill

1. Write the relationship between utilisation and waiting time.
2. Fill in the delay multiples for 50, 70, 80, 90, 95 and 99 percent.
3. Say why the curve is not a straight line, in one sentence about arrivals.
4. Give the utilisation target for user-facing work, for batch work, and for a hard p99 SLA.
5. Say why batch work can run hot, and why that is the biggest cost lever.

### The redundancy drill

1. State what N+1, N+2 and 2N mean.
2. For a fleet of 14 at 65 percent, compute the utilisation after losing one machine and after losing a
   third.
3. Fill in the table of fleet size against the survivors' load increase.
4. Say how this argument pulls against the day 098 vertical-scaling advice, and reconcile them.

### The autoscaling drill

1. List the five stages of autoscaling lag with their durations.
2. Say what the fleet must therefore be able to do unaided.
3. Say what autoscaling actually saves, and where.
4. Give the three-part pattern you would recommend instead of pure autoscaling.

### The three-resources drill

1. Say what each of compute, storage and bandwidth scales with.
2. Say which one cannot be scaled down and what the only lever is.
3. For a text API, a photo product and a logging system, say which binds.
4. Compute bandwidth for 6,000 QPS at 5 KB, 200 KB and 2 MB per response.
5. Say at what bandwidth figure a CDN stops being optional.

### The storage drill

Compute the fully-loaded figure, showing every step:

1. 5 GB/day of rows, one year retention, three replicas.
2. Add indexes.
3. Add free-space headroom.
4. State the total multiplier over the raw data, and name the two steps people omit.
5. Say what the real lever is and why.

### The measurement drill

1. Say how you would obtain the per-server QPS figure.
2. Define the knee and say why capacity is below it rather than at the failure point.
3. Say why this number matters more than any other in the plan.
4. Say what you would tell an interviewer instead of quoting a confident figure.

### The failure drill

For each, say what happens and what you would add:

1. The fleet is sized at 90 percent utilisation and one machine fails.
2. A 3× spike arrives in ten seconds.
3. Fourteen app servers each open twenty database connections.
4. The disk reaches 95 percent full.
5. A third-party API has a 1,000 requests per second quota.
6. The peak factor used in the estimate was 2 and the real one is 6.

Two of the six are not fixed by adding machines. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Build the tree from its preorder and inorder traversals.*
   Why one traversal is never enough with the counter-example, what each list contributes, the non-obvious
   step about preorder finishing the left subtree, both `O(n²)` costs killed before writing, and the
   cursor-ordering rule.

2. *How many servers does this system need?*
   The division done and immediately disowned, the queueing curve with real multiples, N+1 with the failure
   case verified, growth qualified by provisioning speed, the autoscaling-lag caveat, and which of the three
   resources binds.

3. *Could you build the tree from preorder and postorder?*
   No in general, the two-node counter-example, the reason stated in terms of boundaries, and the full-tree
   exception with how the size is found.

---

## Before you move on

- [ ] I can build the two trees that share a preorder and show which traversal separates them.
- [ ] I can say what each of the three traversals contributes.
- [ ] I can explain why the size from inorder also cuts the preorder list.
- [ ] I can name both `O(n²)` costs and the change that fixes each.
- [ ] I know the position map requires unique values, and I say so.
- [ ] I can write the cursor version and say why left must come first.
- [ ] I can state the explicit-index formula in words.
- [ ] I can derive the postorder version rather than copying it.
- [ ] I can give the preorder-plus-postorder counter-example and the exception.
- [ ] I can write the BST range version and say why no second list is needed.
- [ ] I round-trip every reconstruction before trusting it.
- [ ] I never give peak-QPS-over-per-server as a final answer.
- [ ] I can write the queueing relationship and the delay multiples.
- [ ] I can say why batch work can run at 90 percent and user-facing work cannot.
- [ ] I verify the failure case before quoting a fleet size.
- [ ] I can list the five stages of autoscaling lag and say what it really saves.
- [ ] I can say what each of the three resources scales with, and which is a ratchet.
- [ ] I can produce the fully-loaded storage figure and name the two omitted steps.
- [ ] I answered all three questions above out loud.
