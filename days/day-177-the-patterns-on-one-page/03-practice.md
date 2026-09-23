---
day: 177
track: practice
title: "Practice — The pattern index, and monolith versus microservices"
status: written
---

# Day 177 · Practice

**DSA topic:** The twenty patterns, on one page
**System design topic:** Microservices versus monolith, argued both ways

---

## Code these, in this order

**Today the drill is recognition, so the rule changes.** For every problem below: **read the constraints, say
what they forbid, name the pattern and its precondition, and state the cost — all before writing a line.**
**Give yourself ninety seconds for that part and mean it.** The code is the easy half and you have written all
four shapes before.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Longest Substring Without Repeating Characters | LeetCode 3 (Medium) | Sliding window, and the "seen before the window started" line. |
| 2 | Koko Eating Bananas | LeetCode 875 (Medium) | Binary search on the answer — the pattern people fail to recognise. |
| 3 | Daily Temperatures | LeetCode 739 (Medium) | Monotonic stack, and that it holds positions rather than values. |
| 4 | Course Schedule | LeetCode 207 (Medium) | That "prerequisites" means a graph, and cycles mean impossible. |
| 5 | Subarray Sum Equals K | LeetCode 560 (Medium) | Why this is prefix sums and NOT a sliding window. |
| 6 | Coin Change | LeetCode 322 (Medium) | Naming the state before writing the loop, and why greedy fails. |

### On problem 2, notice what you are searching

Nothing here is sorted and nothing is an array lookup. **Say out loud what the search space actually is** — the
possible answers, not the input — **and say why feasibility is monotone.** That sentence is the entire
recognition, and it is the pattern candidates miss most often.

### On problem 5, compare it with problem 1

Both mention subarrays. **Problem 1 is a window and problem 5 is not.** Work out for yourself which property
problem 5 lacks. **Then construct an input with a negative number where the window approach gives the wrong
answer**, and record it.

### On problem 6, break greedy on purpose

Run greedy — largest coin first — on `coins = [1, 3, 4]`, `amount = 6`. **Record what it gives and what the
answer is.** Then say the state sentence for the DP version out loud before you write the loop.

### On all six, score the ninety seconds

```
   For each problem:
   [ ] I read the constraints first
   [ ] I said what they forbid
   [ ] I named the pattern before writing
   [ ] I named its precondition
   [ ] I stated time and space before writing
   [ ] The pattern was right

   6 problems x 6 = 36 ticks.
   30+  the recognition is there.
   20-29 you know the code and are still finding the shape
        by writing. Do the classifier drill below.
   <20  re-read section 3 until the tell arrives before you
        finish reading the problem.
```

### Then the classifier drill

Take twenty problems you have already solved. **Read only the first line of each, and say the pattern out
loud.** Time yourself. **Anything over five seconds goes on a list**, and that list is what you revise.

### Then the confusable-pairs drill

For each pair, give the one question that separates them:

1. Sliding window against prefix sums.
2. Greedy against dynamic programming.
3. Heap against sorting.
4. BFS/DFS against union-find.
5. Two pointers against binary search.
6. Backtracking against dynamic programming.

### Then the precondition drill

Name the precondition for two pointers, sliding window, greedy, Dijkstra and binary search. **For each, give
the input that breaks it** and say whether the failure is a crash or a wrong answer.

### Then the constraint drill

Cover the right-hand column of the constraint table. **Read each constraint and name the intended technique.**
Then do it in reverse: given a technique, say the constraint that would have hinted at it.

### Then the both-sides drill

Pick any system you know. **Argue for splitting it into services for two minutes.** Then argue against, for two
minutes. **Use different arguments, not the same ones inverted.** Then say which you would actually do and what
would change your mind.

### Then the arithmetic drill

Compute end-to-end availability for four, eight and sixteen services at 99.9 percent each. **Convert each to
minutes a month.** Then compute the latency added by eight network calls, and the monthly cross-zone cost from
sixteen terabytes a day.

### Then the boundary drill

Take a system with orders, payments, inventory, recommendations, search and notifications. **Say which of those
must be atomic together** and therefore must not be split apart. Then say which are safe to split first, and
why.

---

### The index drill

1. Name all twenty patterns, in any order.
2. For any five, give the tell in one sentence.
3. For any five, give the cost.
4. Name the pattern for: "next greater element", "minimise the maximum", "return all subsets", "are these two
   connected".

### The procedure drill

1. Give the four questions, in order.
2. Say which is highest value and why.
3. Give four constraints and what each one names.
4. Give four output shapes and what each one names.
5. Say what to do when two patterns both fire.

### The template drill

Write from memory, without looking:

1. The two-pointer loop.
2. The sliding-window skeleton.
3. Binary search on the answer, including the bounds.
4. The monotonic stack loop.
5. BFS with a distance.
6. The backtracking skeleton, including the undo.
7. A one-dimensional DP loop, with the state said aloud first.

### The definitions drill

1. Define monolith and microservices, and say which line is the real definition.
2. Say what a distributed monolith is and why it is the worst option.
3. Say what a modular monolith is and what it buys.
4. Say what "split by business capability, not technical layer" rules out.

### The both-sides drill

1. Four arguments for splitting, each with its condition.
2. Four arguments against, with what each costs.
3. Say which argument for is strongest, and why it is organisational.
4. Say which argument against is strongest, and why it is permanent.

### The saga drill

1. Give a four-step saga with its compensations.
2. Name four things sagas cost you.
3. Say why a refund is not the inverse of a charge.
4. Give the difference between choreography and orchestration.
5. Give the design rule this implies about where boundaries go.

### The arithmetic drill

1. Availability for 1, 4, 8 and 16 services at three nines, in minutes.
2. What each service would need for the whole to stay at 99.9 percent.
3. Latency added by eight network calls, against eight function calls.
4. Monthly cross-zone cost from stated internal traffic.
5. Upkeep hours for forty services, as a fraction of a twelve-person team.
6. Relationships between six, twenty and forty services.

### The migration drill

1. Describe the strangler fig in five steps.
2. Say why a rewrite fails.
3. Say how you choose the first extraction.
4. Name the platform pieces that must exist before service number two.
5. Say when to stop extracting, with a number.

### The break-it drill

For each, say what happens and whether anything reports it:

1. Two pointers on unsorted input.
2. A sliding window on an array containing negatives.
3. Greedy on `coins = [1, 3, 4]`, `amount = 6`.
4. Dijkstra with a negative edge.
5. BFS marking nodes as seen on dequeue.
6. Backtracking without the undo.
7. `out.append(chosen)` instead of `out.append(chosen[:])`.
8. Recursion over a ten-thousand-node linked list.
9. Eight services sharing one database.
10. Splitting orders and payments apart.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Given this problem, which pattern, and why that one?*
   Constraints first and what they forbid; the output shape; the input structure; what the slow version
   repeats; two candidates rather than one; and the precondition stated with the pattern.

2. *What did you actually learn from solving a few hundred problems?*
   Twenty shapes not twenty algorithms; recognition is the skill that fails, not implementation; constraints
   name the intended solution; and almost every pattern is "stop repeating work".

3. *Would you build this as microservices? Now argue the opposite.*
   Both sides at full strength, the availability and latency arithmetic, the transaction cost, the modular
   monolith as the usual answer, and team count as the thing that actually decides.

---

## Before you move on

- [ ] I can name all twenty patterns.
- [ ] For any pattern, I can give the tell in one sentence.
- [ ] I read the constraints before the problem.
- [ ] I can turn six constraints into six intended techniques.
- [ ] I know "return all" means backtracking and "number of ways" means DP.
- [ ] I know a grid is a graph.
- [ ] I hold two or three candidate patterns, not one.
- [ ] I can separate window from prefix sums with one question.
- [ ] I can separate greedy from DP with one question.
- [ ] I can separate heap from sorting, and traversal from union-find.
- [ ] I state the precondition when I name the pattern.
- [ ] I know which preconditions fail silently rather than crashing.
- [ ] I can write all seven templates from memory.
- [ ] I know BFS marks seen on enqueue.
- [ ] I know backtracking needs the undo and the copy.
- [ ] I can give the complexity ladder and read it backwards from a constraint.
- [ ] I can define monolith and microservices, and say which line is the real definition.
- [ ] I know what a distributed monolith is and why it is the worst option.
- [ ] I can give four arguments for splitting, each with its condition.
- [ ] I can give four arguments against, with what each costs.
- [ ] I know why the deployment argument is organisational.
- [ ] I know why the transaction argument is permanent.
- [ ] I can compute availability for eight services and convert it to minutes.
- [ ] I can compute the latency and the cross-zone cost of a split.
- [ ] I know the per-service upkeep cost in hours.
- [ ] I can describe a saga and name four things it costs.
- [ ] I know the design rule that follows from sagas being expensive.
- [ ] I can describe the modular monolith and name two companies that use one.
- [ ] I can describe the strangler fig and say why a rewrite fails.
- [ ] I know team count decides this, not taste.
- [ ] I know putting two services back together is a respectable outcome.
- [ ] I answered all three questions above out loud.
