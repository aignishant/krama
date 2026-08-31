---
day: 99
track: practice
title: "Practice — Binary trees in code"
status: written
---

# Day 099 · Practice

**DSA topic:** Binary trees in code
**System design topic:** Load balancers

---

## Code these, in this order

One rule for the whole set: **write `from_list`, `to_list` and `show` once, keep them in a file, and use
them for every tree problem for the next two weeks.** Fifteen minutes today saves an hour a day
afterwards.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Invert Binary Tree | LeetCode 226 (Easy) | Mutating a tree in place, and whether you can see the result. |
| 2 | Merge Two Binary Trees | LeetCode 617 (Easy) | Building new nodes, and the four `None` cases. |
| 3 | Search in a Binary Search Tree | LeetCode 700 (Easy) | Why this is `O(height)` and plain-tree search is `O(n)`. |
| 4 | Construct String from Binary Tree | LeetCode 606 (Medium) | A different serialisation format, and why the brackets are load-bearing. |

### On problem 1, use your printer

Print the tree before and after. If you cannot see the inversion in the output, your printer is wrong
and that is worth fixing today rather than on day 104.

### On problem 2, enumerate the cases before writing

There are four combinations of the two nodes being `None` or not. Write all four down, then write the
code, then check that the code has exactly those four outcomes.

### On problem 3, say the difference out loud

This is a search *tree*, so it is `O(height)`. Say what you would have had to do if it were a plain
binary tree, and what the complexity would have been.

### On problem 4, notice what the format keeps

LeetCode's list format and this bracket format both describe a tree. Say what each one does about
missing children, and why neither can simply drop them.

---

### The node drill

1. Write the class from memory, with LeetCode's field names.
2. Say why there is no `Tree` class.
3. Say the two things `None` means, and why one base case covers both.
4. Add `__repr__` and say what it saves you from.
5. Say what `__slots__` would change, in bytes per node.

### The building drill

1. Build the same five-node tree three ways: nested, by assignment, and from a list.
2. Say when you would use each.
3. Build a tree with a node that has only a right child, both ways.
4. Say why that shape is the one worth putting in a test.

### The list-format drill

1. Convert `[1, 2, 3, None, None, 4, 5]` into a drawing.
2. Convert your drawing back into a list and check it round-trips.
3. Drop the `None`s from the list and draw what it now means.
4. Say what LeetCode does with trailing `None`s, and give an example.
5. Say why this format is `O(n)` where the index formula is `O(2^h)`.

### The index-formula drill

1. Give the child and parent index formulas.
2. Compute the array size needed for a complete tree of 1,000 nodes.
3. Compute it for a degenerate tree of 20 nodes, and then 40.
4. Say which structure uses this layout deliberately, and why it can.
5. Compare the memory of a million-node pointer tree against a million-entry array.

### The no-parent drill

1. State the three consequences of having no parent pointer.
2. Write `find_with_parent` and say what it does instead.
3. Say what maintaining a real `parent` field would cost.
4. Say when you would actually add one.

### The reference drill

1. Run `backup = root; backup.val = 999` and print `root.val`.
2. Say why that happened, and name the day-091 trap it matches.
3. Write a real deep copy.
4. Run `TreeNode(1) == TreeNode(1)` and say why it is `False`.
5. Say what structural equality requires instead.

### The printer drill

1. Write the nine-line sideways printer from memory.
2. Say which subtree appears above and which below, and why.
3. Say which traversal order the three lines form.
4. Print a seven-node tree and a degenerate one, and say which is easier to read.

### The break-it drill

Trigger each and record the exact output or error:

1. `root.value` on a LeetCode-style node.
2. `root.parent`.
3. `from_list` on `[]` and on `[None]`.
4. Dropping the `None`s from a list and comparing the two trees.
5. Building the index-formula array for a degenerate tree of forty nodes.
6. A recursive `copy_tree` on a chain of 10,000 nodes.

---

### The two-jobs drill

1. Name both jobs of a load balancer and say which matters more, with the reason.
2. Say what a balancer turns *n* unreliable servers into.
3. Say what that claim depends on.

### The layers drill

1. Define layer 4 and layer 7 in one sentence each.
2. Give three things layer 7 can do that layer 4 cannot.
3. Give two reasons to choose layer 4 anyway.
4. Say which requests may be retried and which may not, and why.

### The algorithms drill

For each of the seven algorithms, say how it chooses and give its failure mode:

round robin · weighted round robin · least connections · least response time · random ·
power of two choices · consistent hashing

Then answer: four backends hold 12, 3, 7 and 0 in-flight requests. Where does each algorithm send the
next request?

### The slow-server drill

1. Say what round robin does with a server that is slow but alive.
2. Say what least connections does, and why it needs no decision.
3. Name the extra mechanism you would add on top, and what it tracks.
4. Say what you would change about the health check itself.

### The health-check drill

1. Name the four settings.
2. Write the detection-time formula and compute it for 5 s / 2 / 2 s.
3. Compute the failed requests during that window at 4,000 req/s across 4 backends.
4. Recompute both for a 2-second interval and say what you paid for the improvement.
5. Say why the two thresholds exist and what they are preventing.

### The health-endpoint drill

1. Say what a too-shallow check reports, and what it costs.
2. Say what a too-deep check does when the shared database hiccups.
3. State the rule for what the endpoint should check.
4. Say where the deep checks belong instead.

### The failure drill

For each, say what happens and what you would add:

1. The load balancer itself fails.
2. A deploy kills servers with requests in flight.
3. Sessions live in each server's memory.
4. Every backend is slow because the database is slow.
5. WebSocket connections have been open for six hours and a new server joins.
6. 100,000 clients connect and each one becomes a backend connection.

Two of the six are not solved by the balancer at all. Name them.

### The numbers drill

Compute or state each:

1. Requests per second one layer 7 instance handles.
2. TLS handshakes per second per core, and the effect of keep-alive at 10,000 req/s.
3. Health-check traffic for 20 backends at a 5-second interval.
4. How many balancer instances you run at 6,000 peak QPS, and why that number is not about capacity.
5. Backend connections for 100,000 client connections with a keep-alive pool.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Build this tree in code. Now print it.*
   No `Tree` class and what `None` means, LeetCode's field names, the list format read out with the nulls
   justified, the helpers you would write once, the sideways printer, and the no-parent fact stated before
   it bites.

2. *How does a load balancer decide which server gets the request?*
   Both jobs with the ranking, eligibility separated from choice, health checks with the detection-time
   arithmetic, least connections over round robin with the slow-server reason, the layer with the retry
   justification, and never running just one.

3. *One server is slow but not dead. What happens?*
   Round robin's specific failure, least connections' self-correction, outlier detection as the next step,
   and what you would change about the health check.

---

## Before you move on

- [ ] I have `from_list`, `to_list` and `show` saved in a file I will reuse.
- [ ] I can write the node class from memory with the right field names.
- [ ] I can say the two things `None` means in a tree.
- [ ] I can read a level-order list aloud and draw the tree correctly.
- [ ] I can say why the nulls cannot be dropped, with the specific wrong tree.
- [ ] I know why this format is `O(n)` and the index formula is `O(2^h)`.
- [ ] I can state the three consequences of having no parent pointer.
- [ ] I know what `backup = root` actually does.
- [ ] I know why `TreeNode(1) == TreeNode(1)` is `False`.
- [ ] I can build a deliberately awkward test tree and say why it is better.
- [ ] I can name both jobs of a load balancer and rank them.
- [ ] I can define layer 4 and layer 7 and justify a choice.
- [ ] I can give the failure mode of every algorithm in the table.
- [ ] I can say what round robin does with a slow-but-alive server.
- [ ] I can write the detection-time formula and compute the failed-request count.
- [ ] I can say what the health endpoint must not check, and what happens if it does.
- [ ] I can explain connection draining and why the grace period matters.
- [ ] I can say why sticky sessions are a compromise rather than a design.
- [ ] I answered all three questions above out loud.
