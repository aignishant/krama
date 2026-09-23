---
day: 140
track: practice
title: "Practice — Bipartite graphs and two-colouring"
status: written
---

# Day 140 · Practice

**DSA topic:** Bipartite graphs and two-colouring
**System design topic:** Websockets, long polling, and server-sent events

---

## Code these, in this order

One rule for the whole set: **the conflict test is `colour[neighbour] == colour[vertex]`, not
`colour[neighbour] != -1`.** Write that line first and read it back before filling anything else in. Checking
"already coloured" fails on every even cycle, and a four-vertex ring is the smallest example.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Is Graph Bipartite? | LeetCode 785 (Medium) | The colour check, and the loop over every component. |
| 2 | Possible Bipartition | LeetCode 886 (Medium) | Building the graph in both directions from a dislike list. |
| 3 | Satisfiability of Equality Equations | LeetCode 990 (Medium) | The same idea via Union-Find, with `==` before `!=`. |
| 4 | Maximum Number of Edges to Keep Graph Fully Traversable | LeetCode 1579 (Hard) | Union-Find again — contrast with two-colouring. |
| 5 | Flower Planting With No Adjacent | LeetCode 1042 (Medium) | Four colours, greedy — and why two-colouring does not apply. |

### On problem 1, break the check on purpose

Write the version that returns `False` whenever a neighbour is already coloured. Run it on a four-vertex ring
`0-1-2-3-0`. Record the answer and the correct one. One sentence on what "already coloured" fails to
distinguish.

### On problem 1, break the outer loop on purpose

Build a graph whose first component is a path and whose second is a triangle. Run a version that only colours
from vertex 0. Record the answer.

### On problem 2, break the graph build

Build the adjacency one-directionally and run it on a triangle `[[1,2],[1,3],[2,3]]`. Record the answer.
Say which direction of wrongness that is — a false yes or a false no — and why that is the worse one here.

### On problem 5, say why the phase's tools do not apply

Four colours, and the graph is guaranteed to have degree at most three. Write one sentence saying why greedy
works here and why a two-colouring check would answer the wrong question. Then say what makes the general
three-colour problem hard.

### Then the odd-cycle extractor

Add parent pointers to your problem 1 solution and return the actual odd cycle on failure. Test it on a
triangle, on a five-ring, and on a graph where the cycle is buried three levels deep and reached from two
different branches — that last one is where the common-ancestor walk earns its keep.

### Then the parity Union-Find

Solve problem 2 again with Union-Find plus parity: alongside each element, store the parity of its distance to
its root. Then time both versions on 100,000 constraints delivered one at a time, reporting after each. Two
numbers.

---

### The check drill

1. Write the BFS version from memory.
2. State the conflict condition precisely, and say what it is not.
3. Say why the first colour in a component is arbitrary.
4. Say why the loop runs over every vertex.
5. Say why the colour array replaces the seen set rather than adding to it.

### The odd-cycle drill

1. State the rule in one line.
2. Prove bipartite ⟹ no odd cycle.
3. Prove no odd cycle ⟹ bipartite.
4. Say which of those two the algorithm actually executes.
5. Give the smallest non-bipartite graph, and say why every tree is bipartite.

### The variants drill

1. Return the two sides instead of a boolean.
2. Return the odd cycle, and describe the common-ancestor walk.
3. Describe the Union-Find-with-parity version and when you would use it.
4. Say what changes if the two sides must be equal in size.
5. Say what changes at three colours, and why.

### The costs drill

1. Give time and space, and say why there is no overhead over a plain BFS.
2. Say what the worst case is and when early exit helps.
3. Compare traversal-per-constraint with parity Union-Find at 100,000 constraints.
4. Say why lists beat dictionaries here when vertices are numbered.

### The break-it drill

Trigger each and record the exact output or error:

1. `colour[neighbour] != -1` as the conflict test, on a four-ring.
2. Colouring only from vertex 0, with a triangle in another component.
3. A one-directional graph build, on a triangle.
4. Recursive DFS on a path of 100,000 vertices.
5. Asserting the sides are equal in size, on a star.
6. Two-colouring a graph where the problem allows three groups.

---

### The four-mechanisms drill

1. Describe each of the four in one sentence.
2. Give the two questions that decide between them.
3. Say which two deliver at the same speed and why that surprises people.
4. Say what SSE gives you free that WebSockets do not.
5. Say what WebSockets give you that SSE cannot.

### The polling drill

1. Compute requests per second for 100,000 users at a 5-second interval.
2. Compute the bandwidth, and the waste fraction at a 1% hit rate.
3. Say what happens to load when you halve the latency, and why that never improves.
4. Give two things that make polling much cheaper than its reputation.
5. Name three cases where polling is the correct answer.

### The state drill

1. Say what changes when a fleet holds persistent connections — four things.
2. Explain why cross-server delivery needs a backplane.
3. Say why per-user channels beat a firehose, with the arithmetic.
4. Say why load balancing goes uneven with long-lived connections.
5. Say what capacity is now measured in.

### The delivery drill

1. Say why push is not delivery.
2. Describe the cursor mechanism.
3. Say what SSE provides for this automatically.
4. Describe the gap between catch-up and live, and the fix.
5. Say why the client must deduplicate regardless.
6. Say why Redis pub-sub being fire-and-forget is acceptable here.

### The deploy drill

1. Compute the reconnect rate for 40 servers × 25,000 connections restarted at once.
2. Recompute with 30 seconds of jitter and with a rolling restart.
3. Name the three mitigations and say which must ship first, and why.
4. Say what draining is.

### The numbers drill

1. Compare polling bandwidth against WebSocket bandwidth for the same workload.
2. Give connections per machine and memory per connection.
3. Size the machines for 100,000 and for 1,000,000 concurrent users.
4. Compute backplane load with per-user channels and with a firehose.
5. Compute long polling's memory on a threaded server and on an async one.
6. Give the latency of all four mechanisms.

### The failure drill

For each, say what happens and what you would build:

1. A user's phone enters a tunnel for forty seconds.
2. A deploy restarts every WebSocket server simultaneously.
3. A message is published to Redis while a server is briefly disconnected from it.
4. Every server subscribes to every message.
5. Long polling on a thread-per-request server with 10,000 waiting clients.
6. A WebSocket held open to a device that has been switched off.
7. The app is closed and a message arrives.

Two of the seven are not solvable by any of today's mechanisms. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Can these people be split into two teams with no conflicts?*
   Two-colouring with the precise conflict condition, the arbitrary first colour, the loop over every
   component, the odd-cycle rule with its proof, and returning the sides plus the offending cycle.

2. *Why is it impossible?*
   The odd cycle, both directions of the proof, the five-ring made concrete — and the cliff at three colours
   if they push.

3. *How does the browser find out about a new message?*
   The four mechanisms and the two questions that choose between them, the polling arithmetic, the statefulness
   that persistent connections force, the backplane, and "push is not delivery" with the cursor.

---

## Before you move on

- [ ] My conflict test compares colours, not "is it coloured".
- [ ] I can write the BFS two-colouring from memory.
- [ ] I know the first colour is arbitrary and why.
- [ ] I loop over every vertex and know what a hidden triangle costs.
- [ ] I build undirected graphs in both directions.
- [ ] I can state the odd-cycle rule and prove both directions.
- [ ] I know every tree is bipartite and why.
- [ ] I return the two sides, not a boolean.
- [ ] I can extract the odd cycle with parent pointers.
- [ ] I know the parity Union-Find version and when it wins.
- [ ] I know equal-sized groups is a separate, harder problem.
- [ ] I know three-colouring is NP-complete and why two is not.
- [ ] I can give the cost and say why there is no overhead over BFS.
- [ ] I can describe all four real-time mechanisms.
- [ ] I know the two questions that choose between them.
- [ ] I can compute polling's request rate and waste fraction.
- [ ] I know halving polling latency doubles the load, always.
- [ ] I know what makes polling cheaper than its reputation.
- [ ] I can name three cases where polling is right.
- [ ] I know what SSE gives free and what it cannot do.
- [ ] I know what WebSockets hand back to me to implement.
- [ ] I can name the four things persistent connections change.
- [ ] I can explain the backplane and why per-user channels matter.
- [ ] I know push is not delivery, and can describe the cursor.
- [ ] I know the catch-up-to-live gap and the fix.
- [ ] I can compute the deploy reconnect herd and name three mitigations.
- [ ] I know jittered reconnect must ship in the first release, and why.
- [ ] I know the boundary where platform push notifications take over.
- [ ] I answered all three questions above out loud.
