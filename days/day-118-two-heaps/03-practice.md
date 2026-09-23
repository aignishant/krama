---
day: 118
track: practice
title: "Practice — Two heaps: the running median"
status: written
---

# Day 118 · Practice

**DSA topic:** Two heaps: the running median
**System design topic:** Leader election

---

## Code these, in this order

One rule for the whole set: **assert both invariants after every insertion.** Sizes differ by at most one,
and `max(low) <= min(high)`. Two lines, and they catch every bug in this problem — all of which otherwise
produce a plausible wrong number.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Find Median from Data Stream | LeetCode 295 (Hard) | The two invariants, the negation, and push-shift-rebalance. |
| 2 | IPO | LeetCode 502 (Hard) | Two heaps facing each other with a different question. |
| 3 | Sliding Window Median | LeetCode 480 (Hard) | Lazy deletion, and logical sizes versus `len(heap)`. |
| 4 | Meeting Rooms II | LeetCode 253 (Medium) | The simpler cousin: one heap of end times against a stream of starts. |

### On problem 1, write both versions

Push-shift-rebalance, and the branching version. Run both over ten thousand random values and assert they
agree. Say which you would write in an interview and why.

### On problem 1 again, break it three ways

Remove the rebalance and run 1 to 7. Drop one negation. Make the median function read from the wrong heap
on odd counts. Record all three outputs and say which of them ever raises.

### On problem 3, track the sizes separately

Write it once using `len(heap)` for the rebalance and once using logical counters. Find an input where they
differ and record it.

### On problem 4, notice the shape

Say what the single heap holds, what the boundary is, and why this problem does not need two.

---

### The invariants drill

1. State both invariants.
2. Say what each one buys.
3. Write the two-line assertion.
4. For each invariant, say what breaks if it is violated.

### The structure drill

1. Say which heap is a max-heap and which is a min-heap, and why each way round.
2. Say what the two tops represent.
3. Give the median rule for odd and even counts.
4. Say why the median is `O(1)`.

### The insert drill

1. Write push-shift-rebalance from memory.
2. Explain why pushing into `low` unconditionally is safe.
3. Say which line guarantees the ordering invariant.
4. Write the branching version and name its two extra risks.

### The negation drill

1. Say how many negations there are on the way in, on the way out, and when moving across.
2. Write the line that moves a value from `low` to `high`.
3. Drop a negation and record what the median becomes.

### The convention drill

1. Say which heap holds the extra element on an odd count in your implementation.
2. Say what must agree with that choice.
3. Change one and not the other, and record which counts are now wrong.

### The alternatives drill

1. Give insert and query complexity for four approaches.
2. Compute the element moves for a sorted list at n = 100,000.
3. Say where the crossover with a sorted list actually is, and why.
4. Say what an order-statistic tree gives you that two heaps do not.

### The variants drill

1. Say what changes for the sliding-window version.
2. Say what changes for the 90th percentile.
3. Describe the IPO shape in one sentence.
4. Name the production answer for percentiles at scale, and why.

### The break-it drill

Trigger each and record the exact output or error:

1. No rebalance, on 1 to 7 ascending.
2. `float(self.low[0])` without the negation.
3. The median reading from `high` on an odd count while the rebalance favours `low`.
4. `//` instead of `/` for the even case.
5. The branching version with no empty-heap check, on the first insert.
6. Comparing against `high[0]` instead of `-low[0]` when routing.
7. `len(heap)` instead of logical sizes in the sliding-window version.

---

### The why-a-leader drill

1. Give four things a leader makes cheap.
2. Give four things leaderless gives up.
3. State the trade in one sentence.
4. Name the everyday case where a beginner meets this problem.

### The election drill

1. Describe the sequence from missed heartbeat to new leader.
2. Say what a term is and what changes it.
3. State the two rules that guarantee at most one leader per term.
4. Say why the timeout is randomised, and what happens without it.
5. Give typical figures for the heartbeat, the timeout and the whole failover.

### The split-brain drill

1. Say why a paused leader is indistinguishable from a crashed one.
2. Name three causes of a pause long enough to matter.
3. Describe what the old leader believes when it wakes.
4. Name the three defences and say what each one catches.
5. Say where fencing must be enforced, and why not at the leader.

### The practical drill

1. Say whether you would implement Raft, and why.
2. Describe the etcd approach in three steps.
3. Describe the ZooKeeper approach, including the watch detail.
4. Say where the fencing token comes from in each.
5. State the cost of using an external service, with the Kubernetes example.

### The lease drill

1. Define a lease.
2. Say what it buys over a plain lock.
3. Draw the safety gap and say which way round it must go.
4. Compute a safety margin from clock skew and message delay.
5. Say why a lease does not remove the need for fencing.

### The sizing drill

1. Fill in the nodes-to-tolerated-failures table for 3 through 9.
2. Say why even numbers buy nothing.
3. Say why bigger is not better, in terms of latency.
4. Give the recommended cluster size and the source of that guidance.

### The bottleneck drill

1. Name the two ways a leader is a bottleneck.
2. Give write-rate figures for a relational leader and for etcd.
3. State the standard answer, in four words.
4. Name two systems that do it that way.

### The failure drill

For each, say what happens and what you would add:

1. A JVM full GC pauses the leader for four seconds.
2. All followers have identical election timeouts.
3. Clients find the leader through DNS with a 60-second TTL.
4. A four-node cluster splits two and two.
5. A lock is granted, the holder pauses, and the lock expires mid-operation.
6. A nightly job is deployed to fifty machines with no coordination.

Two of the six are not fixed by a faster election. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the median of a stream of numbers.*
   The split-at-the-boundary idea before the structure, which heap is which and why, both invariants,
   push-shift-rebalance as one unit with the reason the blind push is safe, the negation convention, and
   the comparison against a sorted list.

2. *The leader crashed. How does the cluster choose the next one?*
   The election in one paragraph with terms, majority and randomised timeouts, then the hard half — a
   paused leader is indistinguishable from a dead one — fencing with the enforcement at the storage, and
   what you would actually build.

3. *What if the old leader comes back?*
   Why it happens, what it believes, the three defences, and where each one acts.

---

## Before you move on

- [ ] I can state both median invariants and write the assertion.
- [ ] I know which heap is a max-heap and can say why each way round.
- [ ] I can write push-shift-rebalance from memory and justify the blind push.
- [ ] I know exactly how many negations go where.
- [ ] My median function agrees with my rebalance rule.
- [ ] I ran the version with no rebalance and saw the drift.
- [ ] I can compare against a sorted list with real numbers, and name the crossover.
- [ ] I know what an order-statistic tree adds.
- [ ] I can adapt it to a percentile and to a sliding window.
- [ ] I know the production answer for percentiles at scale.
- [ ] I can say why a leader exists, in terms of coordination.
- [ ] I can describe the election including terms, majority and randomised timeouts.
- [ ] I can say why the randomisation matters.
- [ ] I can explain why a paused leader is indistinguishable from a dead one.
- [ ] I can name three fencing defences and say where each acts.
- [ ] I know that the storage must enforce the token, not the leader.
- [ ] I would use etcd or ZooKeeper, and know where the token comes from.
- [ ] I can draw the lease safety gap the right way round.
- [ ] I know why cluster sizes are odd and why bigger is not better.
- [ ] I can say what usually dominates failover time.
- [ ] I answered all three questions above out loud.
