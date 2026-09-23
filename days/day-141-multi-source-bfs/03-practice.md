---
day: 141
track: practice
title: "Practice — Multi-source BFS and 0-1 BFS"
status: written
---

# Day 141 · Practice

**DSA topic:** Multi-source BFS and 0-1 BFS
**System design topic:** Push notifications, end to end

---

## Code these, in this order

One rule for the whole set: **the loop that finds the sources goes above the BFS loop, never inside it.** Type
the source-collection loop, then a blank line, then `while queue:`. Every problem below is a one-line change
from ordinary BFS, and the line is on the way in.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | 01 Matrix | LeetCode 542 (Medium) | The plainest multi-source: every 0 is a source. |
| 2 | Rotting Oranges | LeetCode 994 (Medium) | Level counting, and the `-1` for what is never reached. |
| 3 | Walls and Gates | LeetCode 286 (Medium) | Many sources, and why one BFS per gate times out. |
| 4 | As Far from Land as Possible | LeetCode 1162 (Medium) | Inverting "for each X find the nearest Y", then `max`. |
| 5 | Minimum Obstacle Removal to Reach Corner | LeetCode 2290 (Hard) | 0-1 BFS with a deque. |
| 6 | Minimum Cost to Make at Least One Valid Path | LeetCode 1368 (Hard) | 0-1 BFS again, with the cost on direction changes. |

### On problem 3, write the slow version and time it

Solve it once with one BFS per gate and a per-cell minimum, and once multi-source. Run both on a
1,000 × 1,000 grid with 500 gates. Record both times and both cell-visit counts. The ratio should be about 500.

### On problem 2, break it three ways

1. Use `while queue:` for the inner loop instead of `for _ in range(len(queue))`. Record the answer.
2. Drop the `and fresh` from the outer condition. Run on `[[2, 1]]` and record the answer.
3. Drop the `-1` check. Run on a grid with a sealed-off fresh orange and record what comes back.

Three wrong answers, all plausible.

### On problem 5, add a `visited` set on purpose

Solve it correctly, then add `if neighbour in visited: continue` to the 0-1 BFS. Find an input where the two
disagree and record both answers. Write one sentence saying why a vertex may need to be processed twice here
and never does in plain BFS.

### On problem 6, count the deque operations

Instrument `appendleft` and `append`. Run on the largest input and record both counts. Then solve it with
Dijkstra and count heap pushes and pops. Compare the totals and say where the `log` factor went.

### Then the three-weights experiment

Take your 0-1 BFS and feed it a graph with weights 0, 1 and 2. Compare its answer against Dijkstra's on the
same graph. Find an input where they differ, and write one sentence naming the invariant that broke.

---

### The multi-source drill

1. Say what the one-line change from ordinary BFS is.
2. Say why no minimum appears anywhere in the code.
3. Say why the cost does not depend on the number of sources.
4. Give the three phrasings that signal this shape.
5. Describe the virtual-source alternative and when you would use it.

### The level-counting drill

1. Write the level-by-level loop from memory.
2. Say why `len(queue)` must be frozen before the inner loop.
3. Say why the outer condition needs `and fresh`.
4. Say where the unreachable check goes and why not inside the loop.

### The 0-1 drill

1. Say why plain BFS breaks when an edge is free.
2. State the deque rule in one line.
3. State the invariant the deque maintains, and why it is the same one a plain queue gives.
4. Say why there is no `visited` set and what the guard is instead.
5. Say what breaks with three distinct weights, and give the two alternatives.

### The costs drill

1. Give multi-source BFS's cost and say what does not appear in it.
2. Compute multi-source against one-BFS-per-source for 500 gates on a million cells.
3. Give 0-1 BFS against Dijkstra at `V = 100,000, E = 300,000`.
4. Say where Dijkstra's `log` factor comes from and why it disappears here.
5. Give the whole family's costs in one list.

### The break-it drill

Trigger each and record the exact output or error:

1. One BFS per source on a 1,000 × 1,000 grid with 500 sources.
2. Sources pushed inside the loop rather than before it.
3. `while queue:` as the inner level loop.
4. The `and fresh` condition removed, on `[[2, 1]]`.
5. The `-1` check removed, with a sealed-off cell.
6. A `visited` set added to 0-1 BFS.
7. 0-1 BFS on a graph with a weight of 2.

---

### The three-hops drill

1. Name the three hops and say which you control.
2. Say why you cannot reach the device directly — two reasons.
3. Say why the OS holds one connection for all apps.
4. Name the two platforms and what FCM can additionally do.

### The token drill

1. Say what a device token is and what it identifies.
2. Give the table's primary key and say why it is not the user.
3. Name the four rules that keep a token store healthy.
4. Say what the only invalidation signal is.
5. Give the token bug that is a security incident, and the step people forget.

### The guarantee drill

1. Say what "accepted" means and what it does not.
2. Say why the push must be a nudge rather than the message.
3. Give the payload limit and say why it reinforces the same rule.
4. List what you can measure and what you cannot.
5. Say what a "delivery rate" dashboard is really showing.

### The controls drill

1. Say what priority does, on both settings, and what abusing it costs.
2. Say what a collapse key does and exactly which notifications it affects.
3. Say what expiry is for and give a case where omitting it hurts.
4. Say what a silent push is and why you cannot rely on it.

### The fan-out drill

1. Compute the time for 10M devices at 200 requests/s per worker, for 1, 100 and 500 workers.
2. Say what actually limits the throughput.
3. Say why you chunk by key range and what `LIMIT/OFFSET` costs.
4. Compute the effect of 40% dead tokens on the same fan-out.
5. Say what you would do about a hundred-second spread on a time-critical alert.

### The fatigue drill

1. Name the five mechanisms for controlling notification volume.
2. Say which one the platform provides and exactly what it does not cover.
3. Give opt-in and open rates, and say why disabling is effectively permanent.
4. Give the sentence you would say to a product manager who wants a daily broadcast.

### The numbers drill

1. Give annual token churn and the two-year effect without pruning.
2. Compute outbound bytes for 10M devices at 1.5 KB and at 0.3 KB.
3. Break end-to-end latency into its stages and name the variable one.
4. Give the database time for scanning 10M tokens by key range.

### The failure drill

For each, say what happens and what you would build:

1. A user reinstalls the app and never opens it again.
2. A phone is switched off for three days with no expiry set.
3. A group of 200 people, one chatty conversation, no per-user cap.
4. A device is sold and the new owner logs in.
5. A silent push relied on for a scheduled refresh.
6. A notification sent while the app is open and connected.
7. Chunking 10M tokens with `LIMIT/OFFSET`.

Two of the seven are security or privacy problems rather than performance. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *How long until every orange rots?*
   Multi-source BFS with all sources pushed before the loop, why no minimum appears, the level-counting form,
   the `-1` case, and the arithmetic against one BFS per source.

2. *You may break at most some walls. Fewest walls to cross the grid?*
   Why plain BFS is wrong, why Dijkstra is more than needed, the deque rule, the two-distinct-distances
   invariant, no `visited` set — and what changes at three weights.

3. *How does a push notification actually reach the device?*
   The three hops and which you control, the token and its silent invalidation, "accepted is not delivered",
   push-as-a-nudge with the 4 KB limit as evidence, and collapse keys plus per-user throttling.

---

## Before you move on

- [ ] I put the source-collection loop above the BFS loop.
- [ ] I can say why multi-source needs no minimum.
- [ ] I know the cost does not depend on the number of sources.
- [ ] I can give the three phrasings that signal this shape.
- [ ] I can write the level-counting loop and know why `len(queue)` is frozen.
- [ ] I know why the outer condition needs `and fresh`.
- [ ] I always answer for what was never reached.
- [ ] I know the virtual-source alternative.
- [ ] I can say why plain BFS breaks on a free edge.
- [ ] I can state the deque rule and the invariant behind it.
- [ ] I know 0-1 BFS has no `visited` set, and what the guard is.
- [ ] I know what breaks at three weights, and both alternatives.
- [ ] I can compute multi-source against per-source with real numbers.
- [ ] I can compute 0-1 BFS against Dijkstra and say where the log went.
- [ ] I know the three hops and which one I control.
- [ ] I know why the device cannot be reached directly.
- [ ] I can describe the token lifecycle end to end.
- [ ] I know the token table is keyed by token, not user.
- [ ] I know the only invalidation signal, and to delete on it.
- [ ] I know the logout step and why omitting it is a security incident.
- [ ] I know "accepted" is not "delivered", and what I cannot measure.
- [ ] I treat the push as a nudge and keep the content in my store.
- [ ] I know what priority does and what abusing it costs.
- [ ] I know exactly which notifications a collapse key affects.
- [ ] I know what expiry prevents.
- [ ] I can compute fan-out time and say what limits it.
- [ ] I chunk by key range, never `LIMIT/OFFSET`.
- [ ] I can quote token churn and its effect on a fan-out.
- [ ] I can name five ways to control notification volume.
- [ ] I answered all three questions above out loud.
