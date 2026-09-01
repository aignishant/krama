---
day: 125
track: practice
title: "Practice — What a graph is, and where graphs hide"
status: written
---

# Day 125 · Practice

**DSA topic:** What a graph is, and where graphs hide
**System design topic:** Retries, backoff, and thundering herds

---

## Code these, in this order

One rule for the whole set, and today it is not about code: **before writing a line, write two sentences at
the top of the file.** "A vertex is ___." "An edge from A to B means ___." Then say whether it is directed,
weighted, cyclic and connected. Four words. If you cannot fill them in, you have not understood the problem
and the code will be a guess.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Find if Path Exists in Graph | LeetCode 1971 (Easy) | Building an undirected adjacency list and not forgetting the second append. |
| 2 | Find the Town Judge | LeetCode 997 (Easy) | In-degree and out-degree, with no traversal at all. |
| 3 | Number of Provinces | LeetCode 547 (Medium) | A matrix that *is* the graph, plus the outer loop over all vertices. |
| 4 | Keys and Rooms | LeetCode 841 (Medium) | Reachability, and noticing that "all rooms" means checking the unreachable ones. |
| 5 | Accounts Merge | LeetCode 721 (Medium) | The modelling move: make the shared property a vertex. |

### On every problem, do the modelling out loud first

For each of the five, write down the two sentences and the four words *before* looking at any solution. Then
compare with what you actually implemented. Problem 5 is the one where a wrong model costs you an hour and a
right model costs you four lines.

### On problem 3, notice what you were given

The input is an adjacency matrix, not an edge list. Say out loud what that means for the cost of scanning
neighbours, and what you would have preferred to be given. Then say why the problem gave you a matrix anyway.

### On problem 5, count the comparisons both ways

Solve it once by comparing every account against every other account, and once by making emails into
vertices. On 1,000 accounts with 3 emails each, count the comparisons for each version. Two numbers.

### Then the recognition exercise

Take these five problem statements. For each, write the two sentences and the four words. Do not solve them.

1. "Given a list of dominoes, can they be arranged in a line so touching ends match?"
2. "Given exchange rates between currencies, is there a sequence of trades that ends with more than you
   started?"
3. "Given a list of people and who reports to whom, how long until a message reaches everyone?"
4. "You can transform a word by changing one letter, if the result is in the dictionary. Fewest steps from A
   to B?"
5. "Given a set of tasks, each taking some time, and which must finish before which, what is the earliest
   everything can be done?"

Two of the five are the same problem in disguise. Say which.

---

### The vocabulary drill

1. Define vertex, edge, path, cycle and degree in one line each.
2. State the four questions you ask about every graph.
3. Give an example of a real relationship that is directed and one that is undirected.
4. Say what in-degree and out-degree are and give a problem where in-degree is the whole answer.
5. Say what dense and sparse mean and roughly where the line is.

### The modelling drill

For each row of the hiding-places table, say the vertices and the edges out loud:

1. Courses and prerequisites.
2. A grid of land and water.
3. Words differing by one letter.
4. Puzzle states and legal moves.
5. Accounts and shared emails.
6. Packages and their requirements.

Then say which of the six are implicit graphs and what that changes.

### The building drill

1. Write `build_undirected` from memory and say which line makes it undirected.
2. Write `build_directed` and say what changes.
3. Write the prerequisites builder and say the direction out loud as a sentence.
4. Say why the prerequisites builder uses `{v: [] for v in range(n)}` instead of `defaultdict`.
5. Write the grid neighbour function from memory.

### The costs drill

1. Give the maximum `E` for an undirected graph on `V` vertices, and for a directed one.
2. Give `E/V` for three real graphs and say what that tells you.
3. Say what `O(V + E)` means in words and why it is a sum.
4. Count out `reachable`'s cost step by step and explain the factor of two.
5. Compute the memory for a million users with 200 friends each, splitting vertices from edges.

### The break-it drill

Trigger each and record the exact output or error:

1. `build_undirected` with the second append removed, then reachability in both directions.
2. `components` on a graph where two vertices appear in no edge.
3. A traversal from one start on a disconnected graph, counting vertices.
4. A recursive walk with no `seen` set, on a graph with a cycle.
5. A list-based adjacency structure on 1-indexed vertex labels.
6. A graph built with a self-loop, then a degree count.

---

### The failure-mode drill

1. Say what retry amplification is in two sentences.
2. Compute the amplification for three layers at three attempts.
3. Say why nobody designed the 27 and why it survives code review.
4. Name the precondition that must hold before any retry is safe.

### The status-code drill

1. List the responses you retry.
2. List the responses you never retry.
3. Say why retrying a `400` is worse than useless.
4. Say what makes a timeout the ambiguous case, and what it needs.

### The jitter drill

1. Give the four backoff strategies in order and say what is wrong with each of the first three.
2. Explain in two sentences why backoff alone does not fix a herd.
3. Write the full-jitter delay expression from memory.
4. Compute the peak-load reduction from jitter on 1,000 clients over a four-second window.
5. Say what AWS found when they compared the schemes.

### The budget drill

1. Define a retry budget in one sentence.
2. Compute total load with and without a 10% budget when everything fails.
3. Say why a budget beats tuning the attempt count.
4. Name two systems that implement it and what they call it.

### The other-herds drill

For each, say the cause and the fix:

1. A popular cache key expires.
2. Two hundred instances restart after a deploy.
3. Ten million devices sync at midnight.
4. A load balancer restarts and every WebSocket reconnects.

Then say which one you cannot fix after the fact, and why.

### The numbers drill

1. Compute requests per second at the database for 1,000 user actions with 27× amplification.
2. Compute the success rate for 1, 2, 3 and 4 attempts at a 1% independent failure rate.
3. Say which assumption in that calculation fails during a real outage.
4. Size a cache stampede: 10,000 requests a second, 50 ms refill.
5. Compute the mean added latency of three attempts with full jitter at base 100 ms.

### The trade-offs drill

1. Say what every retry costs and when it costs it.
2. Say what backoff trades away, and the arithmetic that has to close.
3. Say which layer should retry and why that one.
4. Say what jitter costs you operationally, and how you mitigate it.
5. Say what a circuit breaker does that no retry policy can.
6. Name the three cases where the right number of retries is zero.

### The failure drill

For each, say what happens and what you would build:

1. Every layer in a four-layer stack has retries enabled by default.
2. A thousand clients fail at the same instant with plain exponential backoff.
3. A payment gateway degrades for ten minutes and the client retries three times per request.
4. A non-idempotent charge endpoint is retried after a timeout.
5. A million cache keys are warmed at startup with an identical TTL.
6. A client-side reconnect with no jitter, after a load balancer restart.
7. Retries configured with a 5-second cap behind a 2-second user timeout.

Two of the seven cannot be fixed by tuning any number. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Is this a graph problem? What are the vertices and edges?*
   The two sentences, the four classification words, and the reason: the question is about following the
   relationships, not about any single one of them.

2. *Given accounts with emails, merge the ones belonging to the same person.*
   The naive quadratic model, then the move that fixes it — make the shared property a vertex — then
   connected components, the not-connected warning, and the name trap.

3. *Everything retried at once and the service died. What went wrong?*
   Amplification with the 27, then the three fixes: full jitter with the peak-load number, a retry budget
   with the 1.1× number, and retrying at exactly one layer. Idempotency named as the precondition.

---

## Before you move on

- [ ] I can define vertex, edge, path, cycle and degree without hesitating.
- [ ] I ask the four questions about every graph before writing code.
- [ ] I write the two modelling sentences before any line of code.
- [ ] I know which line makes an adjacency list undirected.
- [ ] I know why a vertex with no edges can be missing from a `defaultdict`.
- [ ] I never assume a graph is connected.
- [ ] I know every graph traversal needs a `seen` set, and why trees did not.
- [ ] I can recognise an implicit graph and say what changes.
- [ ] I can name six places graphs hide, with vertices and edges for each.
- [ ] I can give the maximum `E` for directed and undirected graphs.
- [ ] I can explain `O(V + E)` in words and say why it is a sum.
- [ ] I can compute the memory split between vertices and edges.
- [ ] I solved Accounts Merge with emails as vertices.
- [ ] I can say what retry amplification is and compute it for three layers.
- [ ] I know exactly which responses to retry and which never to.
- [ ] I know idempotency is a precondition, not an extra.
- [ ] I can explain why backoff without jitter does not fix a herd.
- [ ] I can write the full-jitter delay expression from memory.
- [ ] I can quote the peak-load reduction jitter buys.
- [ ] I can define a retry budget and give the 1.1× versus 4× numbers.
- [ ] I know retries belong at exactly one layer, and which one.
- [ ] I can name four other herds and their fixes.
- [ ] I know which herd cannot be fixed after the fact.
- [ ] I can say what a circuit breaker does that retries cannot.
- [ ] I can name three cases where zero retries is correct.
- [ ] I answered all three questions above out loud.
