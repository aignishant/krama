---
day: 112
track: practice
title: "Practice — Trees revision and mock round"
status: written
---

# Day 112 · Practice

**DSA topic:** Trees revision and mock round
**System design topic:** Scaling revision and interview questions

---

## Code these, in this order

This is a mock round. **Twenty-five minutes each, out loud, no references.** Before writing anything, ask
the five questions and name the shape. If naming the shape takes more than thirty seconds, that — not the
code — is what to practise.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Count Good Nodes in Binary Tree | LeetCode 1448 (Medium) | Recognising "carry state down" from an unfamiliar phrasing. |
| 2 | Maximum Level Sum of a Binary Tree | LeetCode 1161 (Medium) | Recognising a level problem, and the boundary capture. |
| 3 | Sum Root to Leaf Numbers | LeetCode 129 (Medium) | State down again, and the leaf test. |
| 4 | Binary Tree Maximum Path Sum | LeetCode 124 (Hard) | The return-value trick, cold, with the floor and the `-inf`. |

### Before each problem, say the five questions

Search tree? Two trees? Levels? Does a node need something an ancestor knows? Do I need two different
values? Time yourself. Forty seconds or less.

### On problem 4, run the checklist before declaring done

`None` case with the right identity · local versus global · return differs from record · am I
recomputing · is it a copy. Ten seconds, and it catches four silent bugs.

### After all four, write the shape table from memory

Six rows: information direction, shape name, traversal, two examples each. If any row is missing, that is
the day to re-read.

---

### The one-question drill

1. State the question that picks the shape.
2. Give the four directions information can travel and the six shapes they produce.
3. For each shape, give the traversal and two problems.
4. Say which shape is the most used, and why.

### The skeleton drill

1. Write the five-line skeleton from memory.
2. Say what determines the base case, in one word.
3. Give the base case for: height, count, sum, "do all nodes satisfy P", "does any node satisfy P".
4. Say which of the six shapes are exactly this skeleton with different blanks.

### The recognition drill

For each phrasing, name the shape in under ten seconds:

1. "the longest path between any two nodes"
2. "every root-to-leaf path summing to X"
3. "the value of each level's largest node"
4. "is this tree a mirror of itself"
5. "the k-th smallest value"
6. "the deepest leaves' common ancestor"
7. "count nodes greater than everything above them"
8. "the shallowest leaf"

### The return-versus-record drill

1. State the technique in one sentence.
2. Fill in the table for diameter, max path sum, balanced, longest univalue path and largest BST subtree.
3. Say why the parent cannot use the recorded value.
4. Say what happens if you return the recorded value instead.

### The five-bugs drill

1. Name all five bugs.
2. Say which one raises and which four are silent.
3. For each, give the specific wrong output it produces.
4. Run the checklist on a solution you have already written.

### The complexity drill

1. Fill in the complexity table for all fourteen problem families.
2. Identify the three rows that are the same underlying mistake.
3. State the DFS and BFS space costs and the two shapes where each is disastrous.
4. Give the heights for balanced, random and degenerate trees at a million nodes.

### The convention drill

1. Give both height conventions and their base cases.
2. Do the same for diameter.
3. Say the sentence you would use in an interview to settle it.
4. Mix them deliberately on a five-node tree and record how wrong the answer is.

### The mock drill

Do two of these cold, timed, out loud, with no notes:

- Path Sum III (LeetCode 437)
- All Nodes Distance K in Binary Tree (LeetCode 863)
- Vertical Order Traversal (LeetCode 987)
- Delete Nodes and Return Forest (LeetCode 1110)
- Maximum Difference Between Node and Ancestor (LeetCode 1026)

Afterwards write down: how long the first minute took, whether you named the shape before coding, and
whether you stated both complexities without being asked.

---

### The diagnosis drill

1. Name the four diagnostic questions in order.
2. For each, say what the answer eliminates.
3. Say the sentence that disposes of the latency case.
4. Name the resource whose saturation none of the ladder fixes.

### The ladder drill

1. List all ten rungs in order.
2. For each, give the time cost and the leverage.
3. Say which two rungs hold most of the leverage, and why.
4. Say the rule for when to go down a rung.

### The price drill

For each move, name the price without looking:

cache · CDN · statelessness · read replicas · queue · sharding · multi-region · scaling up

Then say which single sentence describes the pattern across all of them.

### The ceiling drill

State the ceiling for each:

1. Vertical scaling — two numbers.
2. Read replicas — and the sentence that explains it.
3. One relational database, reads and writes.
4. One app server.
5. Autoscaling reaction time.
6. DNS-based failover.

### The numbers drill

From memory:

1. The three requests-per-day to QPS conversions.
2. Six machine capacities.
3. The utilisation table and the target, with the reason.
4. Downtime per year at five availability levels.
5. Series and parallel availability for six and two components.
6. What plain modulo costs at 8 → 9 machines, and what the fix costs.

### The four-systems drill

For each, give the read:write ratio, the binding constraint, and the first two moves:

1. A read-heavy feed.
2. A chat system.
3. An e-commerce checkout.
4. An analytics pipeline.

### The mock drill

Do the full ten-minute walkthrough out loud for each, with a timer:

1. *"This service is falling over at 10,000 QPS."*
2. *"Same, but it is a chat system."*
3. *"Same, but the load is a spike at 10 a.m. every day."*
4. *"Same, but writes are 8,000 a second."*

For each, say at which rung you stop and why.

### The availability drill

1. Compute the availability of six components in series at 99.9% each.
2. Say what making one of them optional is worth, in hours per year.
3. Compute two parallel copies at 99.9%, and again with 10% correlation.
4. Say why a scaling change can make a system less available, and what to do about it.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Two problems, no hints, talk as you go.*
   For each: the five questions asked, the shape named before any code, the base case justified as an
   identity, both complexities stated unprompted, the depth risk flagged if the constraints allow it, and
   the five-bug checklist run before declaring done.

2. *This service is falling over at 10,000 QPS. Walk me through fixing it.*
   The four diagnostic questions before anything, the free wins before architecture, cache with the tenfold
   number, the CDN if there is media, the tier count at 65 percent with the queueing reason, replicas with
   the lag price, a queue for the asynchronous work, and an explicit refusal to shard with the threshold
   that would change it.

3. *Would you shard?*
   Not yet, and why — writes are the ceiling that matters, the threshold, and the permanent cost stated in
   three specific losses.

---

## Before you move on

- [ ] I can state the one question that picks the tree shape.
- [ ] I can write the six-row shape table from memory.
- [ ] I can write the five-line skeleton and justify the base case as an identity.
- [ ] I can name the shape for eight unfamiliar phrasings in under ten seconds each.
- [ ] I can state the return-versus-record sentence and fill in its table.
- [ ] I can name the five bugs and say which four are silent.
- [ ] I run the checklist before saying a solution is done.
- [ ] I can fill in the complexity table and spot the three rows that share a mistake.
- [ ] I state DFS and BFS space costs together, with the shapes where each fails.
- [ ] I declare the height convention before writing a base case.
- [ ] I did two unseen problems cold and named the shape in the first thirty seconds.
- [ ] I can name the four diagnostic questions and what each eliminates.
- [ ] I can list all ten rungs of the ladder in order.
- [ ] I can name the price of every move without looking.
- [ ] I can state the ceiling of every rung.
- [ ] I know why replicas stop helping, in one sentence.
- [ ] I can produce all the numbers from memory.
- [ ] I can walk through the 10,000 QPS mock in ten minutes.
- [ ] I refuse to shard first, and can say exactly when I would.
- [ ] I check whether my scaling changes made availability worse.
- [ ] I answered all three questions above out loud.
