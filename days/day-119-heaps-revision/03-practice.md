---
day: 119
track: practice
title: "Practice — Heaps revision and mock round"
status: written
---

# Day 119 · Practice

**DSA topic:** Heaps revision and mock round
**System design topic:** Consensus, and Raft in plain English

---

## Code these, in this order

One rule for the whole set: **before writing a line, say which of the five shapes it is and how big the
heap will be.** Out loud. If you cannot name the shape, you have not recognised the problem yet, and
starting to type is the worst thing you can do.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Kth Largest Element in an Array | LeetCode 215 (Medium) | Shape 2, and whether you reach for quickselect. |
| 2 | Task Scheduler | LeetCode 621 (Medium) | Shape 1 plus a cooldown queue. Today's mock 1. |
| 3 | Find K Pairs with Smallest Sums | LeetCode 373 (Medium) | Shape 4 in disguise. Today's mock 2. |
| 4 | Network Delay Time | LeetCode 743 (Medium) | Shape 5 — Dijkstra with lazy deletion. |
| 5 | Reorganize String | LeetCode 767 (Medium) | Shape 1, and knowing when it is impossible. |

### Say the shape first, every time

Write the shape number and the heap size as a comment on line one, before any code. Five problems, five
comments. Then check them against the lesson.

### On problem 1, write three solutions

Sort, heap, quickselect. Time all three at n = 1,000,000 with k = 10 and again with k = 500,000. Six
numbers. Say where the crossover is and why the ordering changes.

### On problem 3, do the reframing out loud

Before coding, say the sentence that turns it into a merge. If you cannot produce that sentence, the code
will not come either.

### On problem 4, delete the stale check

Remove the `if distance > best[place]: continue` line. Record whether the answer changes and what happens
to the running time. Say why the answer is what it is.

### On problem 5, find the impossible case

Construct an input that cannot be reorganised. State the condition in one line of arithmetic.

---

### The recognition drill

1. State the recognition question in one sentence.
2. Give the three phrasings problems use instead of saying "heap".
3. Give four situations where a heap is the wrong tool.
4. For each of the five problems above, name the shape without looking.

### The five shapes drill

1. Name all five from memory.
2. For each: what the heap holds, its size, the cost, one example.
3. Say which three keep the heap small, and why that is the important column.
4. Give a problem for each shape that is not in the lesson.

### The k-trap drill

1. Say which kind of heap you keep for the k largest, and why.
2. Say it again for the k smallest.
3. Give the one-sentence reason that makes it stop feeling backwards.
4. Write both loops from memory.

### The heapify drill

1. Give the cost of `heapify` and of n pushes.
2. Draw the level-by-level work table for n = 1,000,000.
3. Say why half the nodes contribute zero.
4. Give the ratio between the two approaches at a million elements.

### The cost drill

1. Recite the cost table: push, pop, peek, heapify, find, delete.
2. Say why find is `O(n)` and not `O(log n)`.
3. Compute comparisons for n = 1,000,000 at k = 10, 1,000 and 500,000.
4. Say which argument you lead with in an interview, and why it is not time.

### The heapq drill

1. List the six gotchas from memory.
2. Say what `heapq.heapify` returns.
3. Say how many negations a max-heap needs, and where.
4. Say when `len(heap)` is not the size.
5. Write the max-heap-of-tuples push and read, with both negations.

### The alternatives drill

1. Compare heap and quickselect on four axes.
2. Say when quickselect wins and when it cannot be used at all.
3. Say what to do when k is larger than n/2.
4. Say what you would use if items' priorities change, and give both options.

### The break-it drill

Trigger each and record the exact output or error:

1. `heap = heapq.heapify([3,1,2])` then `heap[0]`.
2. A max-heap read without negating back.
3. `(1, some_object)` pushed twice with equal first fields.
4. `heapq.heappop([])`.
5. Reading `heap[1]` expecting the second-smallest.
6. A max-heap of size k used for the k largest.
7. Dijkstra with the stale check removed, on a dense graph.

### The mock drill

Redo both mock problems from the lesson, timed, twenty minutes each, talking the whole time. Then:

1. For mock 1, say what the negation does to `+1` and why `if remaining:` is correct.
2. For mock 1, state the closed-form formula and say why you would still write the simulation.
3. For mock 2, say why the heap is seeded with `min(len(a), k)` entries and not `len(a)`.
4. For mock 2, say the reframing sentence in under ten words.

---

### The consensus drill

1. Define consensus and give its three properties.
2. Say why single-value consensus is not what real systems need.
3. Explain state machine replication in two sentences.
4. Give the example that shows why order matters, with numbers.
5. Name five different questions that are all the same consensus problem.

### The three-parts drill

1. Name Raft's three parts in order.
2. Say what each one guarantees and what breaks without it.
3. Say which two make it work and which one makes it correct.
4. Say which part most explanations skip.

### The commit drill

1. Define committed.
2. Draw the five-machine picture with three acknowledgements.
3. Give the overlap argument for why commitment is permanent.
4. Say what the leader does before answering the client.
5. Say why two slow followers are not an error condition.

### The safety drill

1. State the election restriction and the everyday phrasing for it.
2. Say how the up-to-date comparison is ordered, and why term comes first.
3. State the current-term commit restriction.
4. Say what goes wrong without it, in one sentence.
5. Say which of the two is more commonly omitted in hand-rolled implementations.

### The log-matching drill

1. State the log-matching property.
2. Walk through the repair example step by step.
3. Say what happens to the follower's diverged entries and why that is safe.
4. Say why naive backtracking is slow and what real implementations do instead.
5. Say why `(index, term)` and not index alone identifies an entry.

### The state-machine drill

1. Name the three states and the four transitions.
2. Say what triggers each transition.
3. Say what a leader does on seeing a higher term, and why it does not argue.
4. Say why that single rule stops a returning old leader from fighting.

### The client drill

1. Name the three problems Raft does not solve for the client.
2. Say how a client finds the leader.
3. Say why a committed command can be applied twice and how to prevent it.
4. Give the three options for reads, with the cost of each.
5. Say why a partitioned leader can serve a stale read.

### The numbers drill

1. Break a single write into its six steps with timings.
2. Say what dominates in one data centre, and what dominates across regions.
3. Compute cross-region write latency for a three-region cluster.
4. Give etcd's write and read throughput ranges.
5. Give the algorithmic failover time and the observed one, and explain the gap.
6. Give etcd's storage quota and say what that implies about what belongs in it.

### The trade-offs drill

1. Fill in the quorum-versus-consensus table on seven rows.
2. State the trade in one sentence.
3. Say where Raft sits on CAP and what the minority side does.
4. Name five things consensus does not give you.
5. Give five situations where you would not use consensus.
6. Compare Raft, Paxos and ZAB in four sentences and stop.

### The failure drill

For each, say what happens and what you would do:

1. A follower is a thousand entries behind and the leader has already snapshotted past them.
2. The leader commits an entry, then crashes before answering; the client retries.
3. A new leader finds an entry from an old term sitting on a majority.
4. A three-node cluster is partitioned one and two.
5. A client reads from a leader that was partitioned away four seconds ago.
6. Someone proposes putting two terabytes of user data behind one Raft group.

Two of the six are not consensus failures at all. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the k most frequent elements in a stream.*
   The recognition question first, then the shape, then the min-heap trap named as a trap, `O(n log k)` time
   with `O(k)` space and the space led with, and the streaming argument as the closing reason.

2. *Explain Raft.*
   Consensus defined, the log as the real answer with state machine replication, the three parts in order,
   both safety restrictions, the cost with the disk sync named as the dominant term, and CP stated plainly.

3. *When would you not use consensus?*
   Five situations, the quorum comparison, and "I would not implement Raft — I would run etcd" with the
   reason.

---

## Before you move on

- [ ] I can state the recognition question in one sentence.
- [ ] I can name all five shapes and what each heap holds.
- [ ] I say the shape and the heap size before I write any code.
- [ ] I know that k largest means a min-heap, and why.
- [ ] I lead with space, not time, when justifying a heap.
- [ ] I can make the streaming argument.
- [ ] I can explain why heapify is `O(n)` with the level table.
- [ ] I know all six `heapq` gotchas without looking.
- [ ] I know a heap cannot find or update an arbitrary element, and both workarounds.
- [ ] I can compare heap with quickselect and say when each wins.
- [ ] I know four situations where a heap is the wrong tool.
- [ ] I solved both mock problems in twenty minutes each, talking out loud.
- [ ] I can define consensus and its three properties.
- [ ] I can explain state machine replication in two sentences.
- [ ] I get to the log quickly, not just the election.
- [ ] I can name Raft's three parts and what each guarantees.
- [ ] I can define committed and give the overlap argument.
- [ ] I can state both safety restrictions and what each prevents.
- [ ] I can state the log-matching property and walk through a repair.
- [ ] I know a leader steps down on a higher term without arguing.
- [ ] I know consensus gives ordering, not exactly-once execution.
- [ ] I know the disk sync dominates a single-region write.
- [ ] I can explain why observed failover is seconds, not milliseconds.
- [ ] I know consensus holds configuration, not data, and the size limit.
- [ ] I can say when I would use a quorum instead.
- [ ] I would run etcd rather than implement Raft, and can say why.
- [ ] I answered all three questions above out loud.
