---
day: 111
track: practice
title: "Practice — Serialising and deserialising a tree"
status: written
---

# Day 111 · Practice

**DSA topic:** Serialising and deserialising a tree
**System design topic:** Single points of failure

---

## Code these, in this order

One rule for the whole set: **say the four decisions out loud before writing** — traversal order, null
marker, delimiter, and how you consume the string. Every bug in this problem is one of those four made
carelessly.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Serialize and Deserialize Binary Tree | LeetCode 297 (Hard) | Null markers, the delimiter, and consuming with an iterator. |
| 2 | Serialize and Deserialize BST | LeetCode 449 (Medium) | Why a BST needs no markers, and the range walk. |
| 3 | Find Duplicate Subtrees | LeetCode 652 (Medium) | Serialisation as a *key* — where the delimiter bug bites hardest. |
| 4 | Construct String from Binary Tree | LeetCode 606 (Medium) | A different format, and why its brackets are load-bearing. |

### On problem 1, break it three ways

Remove the markers and serialise both one-child trees — record the collision. Remove the delimiter and
serialise a tree containing 12 — record the string. Swap the left and right recursion in the
deserialiser — record the tree.

### On problem 1 again, time both traps

Build a 100,000-node tree. Serialise with `+=` and with `join`. Deserialise with `list.pop(0)` and with an
iterator. Record all four times.

### On problem 2, compare the sizes

Serialise the same BST with both codecs and count the tokens. State the ratio and say where the saving
comes from.

### On problem 3, notice why it is the same problem

The subtree signature must be unique per shape *and* values. Say which of the four decisions this problem
punishes hardest, and construct an input that breaks a careless implementation.

---

### The four-decisions drill

1. Name all four decisions.
2. For each, state the constraint and one failing choice.
3. Say which of the four is invisible on single-digit test data.
4. Add a fifth decision about malformed input and say what you would do.

### The markers drill

1. Build both one-child trees and serialise them with and without markers.
2. Say what the marker actually encodes, in one sentence.
3. Compute the number of markers for a tree of `n` nodes, and prove it.
4. Reconcile this with day 110's "one traversal is never enough".

### The delimiter drill

1. Serialise a tree containing 12 without a delimiter and read the result back by hand.
2. Do the same for a tree containing −1.
3. State the rule for a valid delimiter and for a valid null marker.
4. Say what you would do if the values were arbitrary strings.

### The consumption drill

1. Write the deserialiser with an iterator.
2. Rewrite it with `list.pop(0)` and time both at 100,000 tokens.
3. Say why the slow one raises nothing.
4. Name two other correct approaches.

### The order drill

1. Write the preorder codec and the level-order codec.
2. Serialise a perfect tree of 7 and a right-chain of 7 with both, and count tokens.
3. Say which format wins on which shape.
4. Say which one you would write, and why.

### The BST drill

1. Write the BST codec without markers.
2. Say why the markers are unnecessary, in one sentence about ordering.
3. Give the token counts for both codecs on the same BST.
4. Say what the range walk has in common with day 108.

### The compactness drill

1. Give three ways to make the output smaller, in increasing order of effort.
2. State the information-theoretic floor for the shape and where it comes from.
3. Compute the text size for a million integers and compare with a binary encoding.
4. Say why knowing the floor is useful.

### The break-it drill

Trigger each and record the exact output or error:

1. No null markers, on the two one-child trees.
2. No delimiter, on a tree containing 12.
3. `-1` used as the null marker, on a tree containing −1.
4. `list.pop(0)` on a 100,000-token string, timed.
5. String `+=` on a 100,000-node tree, timed.
6. Right recursion before left in the deserialiser.
7. `deserialise("")` and `serialise(None)`.
8. A recursive codec on a 10,000-node chain.

---

### The method drill

1. State the two passes for finding SPOFs.
2. Say what the second pass finds that the first cannot.
3. Do both passes on a diagram with a load balancer, three app servers, a cache and a database.
4. Say what question you ask about every redundant pair.

### The undrawn drill

1. Name seven dependencies that are usually not on a diagram.
2. For each, say what specifically breaks when it fails.
3. Say which one does not affect running instances but stops recovery.
4. Say which one is the purest correlated failure and why.

### The arithmetic drill

Compute each:

1. Downtime per year at 99%, 99.9%, 99.95%, 99.99% and 99.999%.
2. The product of six components at 99.99, 99.99, 99.95, 99.9, 99.95 and 99.95.
3. The combined availability of two and three parallel copies at 99.9%.
4. The same with 10% correlation, and the ratio to the naive figure.
5. The availability gain from making one 99.9% component optional.

### The three-responses drill

1. Define redundancy, failover and degradation.
2. Say what redundancy alone achieves.
3. For each of these, choose one and justify it: recommendations service, database primary, one app
   server, search, the payment provider.
4. Say what makes a failover real rather than nominal.

### The correlation drill

1. Name six ways two "independent" components can fail together.
2. Say which one redundancy cannot help with at all, and why.
3. Say what practice therefore counts as availability work.
4. Explain the village's approach road in one sentence of system terms.

### The blast-radius drill

1. Name the four levers in increasing order of effort.
2. Give the percentage of users affected for a single stack, two regions, ten cells and a hundred cells.
3. Explain shuffle sharding and compute the overlap for 5 servers out of 100.
4. Say what a bulkhead is and what a circuit breaker converts one failure into.
5. Say why a slow dependency is more dangerous than a dead one.

### The failover-time drill

1. List the five components of failover time.
2. Say which is usually the largest, and that it is a configuration choice.
3. Compute a proxy-based and a DNS-based failover time.
4. Name six reasons an untested failover does not work.

### The failure drill

For each, say what happens and what you would add:

1. A certificate used by every service expires at midnight.
2. A bad configuration is pushed to all replicas.
3. A downstream dependency slows from 50 ms to 5 seconds.
4. The config service is unavailable during an autoscaling event.
5. One engineer who knows the failover procedure is unreachable.
6. Two "redundant" servers are in the same rack.

Three of the six are not fixed by adding a redundant copy. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Serialise this tree, then rebuild it from the string.*
   The four decisions framed as design, why markers make one traversal sufficient with the collision shown,
   preorder chosen for what it does to deserialisation, the marker and delimiter constraints, the two
   `O(n²)` traps named before writing, and the BST halving offered.

2. *Which component here takes the whole system down if it fails?*
   The two-pass method rather than a list, the drawn ones quickly, the undrawn ones at length, the series
   arithmetic with the two-days-a-year figure, the three distinct responses, and the independence question
   for every redundant pair.

3. *You have two of those. So what?*
   Detection, switching and currency — with the DNS TTL as the usual largest term, and the six reasons an
   untested failover fails.

---

## Before you move on

- [ ] I state the four serialisation decisions before writing any code.
- [ ] I can show the collision that markers prevent.
- [ ] I can compute the number of markers for `n` nodes and explain it.
- [ ] I can reconcile "one traversal is never enough" with "one traversal plus markers is".
- [ ] I know which marker and delimiter choices are unsafe, and why.
- [ ] I use an iterator and can quote the cost of `pop(0)`.
- [ ] I join once and can quote the cost of `+=`.
- [ ] I can write the BST codec and say why it needs no markers.
- [ ] I know the token counts for both codecs and the ratio.
- [ ] I can name the information-theoretic floor for the shape.
- [ ] I have an iterative codec for deep trees.
- [ ] I can state the two-pass method for finding SPOFs.
- [ ] I can name seven undrawn dependencies and what each one breaks.
- [ ] I can do the series and parallel arithmetic in both directions.
- [ ] I can compute what 10% correlation does to a redundant pair.
- [ ] I can distinguish redundancy, failover and degradation with examples.
- [ ] I ask whether every redundant pair fails independently.
- [ ] I can name the four blast-radius levers and explain shuffle sharding.
- [ ] I can say why a slow dependency is worse than a dead one.
- [ ] I answered all three questions above out loud.
