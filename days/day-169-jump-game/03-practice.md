---
day: 169
track: practice
title: "Practice — Jump game and reachability"
status: written
---

# Day 169 · Practice

**DSA topic:** Jump game and reachability
**System design topic:** Design a distributed job scheduler

---

## Code these, in this order

One rule for the whole set: **before writing a line, say what single number you are carrying.** Every problem
here collapses a set into one value — the furthest reachable index, the end of the current level, the largest
gap. **If you cannot name the number and say why the set collapses to it, you are about to write a set.**

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Jump Game | LeetCode 55 (Medium) | The collapse: a reachable set that is a prefix. |
| 2 | Jump Game II | LeetCode 45 (Medium) | BFS levels without a queue, and the loop bound. |
| 3 | Gas Station | LeetCode 134 (Medium) | The same frontier idea wearing a different hat. |
| 4 | Jump Game III | LeetCode 1306 (Medium) | Where the collapse fails — and you need a real search. |
| 5 | Jump Game VI | LeetCode 1696 (Medium) | Reachability plus a value, so greedy dies and a deque arrives. |
| 6 | Minimum Number of Taps to Water a Garden | LeetCode 1326 (Hard) | Jump Game II in disguise, with intervals. |

### On problem 1, delete the guard

Remove `if i > furthest: return False` and run on `[0, 1]` and `[3, 2, 1, 0, 4]`. **Record what each returns.**
Then say in one sentence what the loop is doing after position 0 on the first input, and why nothing complains.

### On problem 1, prove the prefix claim

Say out loud why the reachable set is always a prefix of the array. **Then construct an input where it is not**
— you cannot, with non-negative jumps. **Say what would have to change for it to fail**, and connect that to
problem 4.

### On problem 2, get the loop bound wrong on purpose

Iterate to `len(nums)` instead of `len(nums) - 1`. Run on `[2, 3, 1, 1, 4]` and on `[2, 1]`. **Record both
answers.** One is wrong and one is right — say why, and say what that means for a test set of three cases.

### On problem 2, name the BFS

Write the explicit BFS with a queue that answers the same question. Run both on the same input and check they
agree. **Then say which two variables in the greedy version are the queue**, and why the levels are contiguous.

### On problem 3, find the frontier

Gas Station does not look like jumping. **Say what the running total is, and what resetting it to zero at a
negative means.** Then say why the answer index is the one after the last reset, and why one pass suffices.

### On problem 4, say why greedy dies

Jumps go both directions here. **Say precisely which property broke** — name it — and why the reachable set is
no longer a prefix. Then write the BFS. **Compare its shape to your problem-2 solution and say what was
implicit there.**

### On problem 5, add a cost

Now each landing has a value and you want the best total. **Say why the furthest-reach heuristic gives the
wrong answer**, and construct a small input where it does. Then write the DP with a monotonic deque.

### On problem 6, do the translation explicitly

Convert each tap to an interval, then to a jump array. **Write down the conversion before coding it.** Solve it
with your problem-2 code unchanged. **Then solve it directly on intervals** and say which you would write in an
interview.

### Then the counter-example drill

Build a version of Jump Game II where each jump has a cost and greedy loses. **Write the `O(n^2)` DP and the
greedy side by side** and search random inputs until they disagree. Record the smallest disagreement you find.

### Then the verification drill

Write the `O(n^2)` DP for minimum jumps. Check the greedy against it on two thousand random arrays with a fixed
seed. **Say why zero mismatches is evidence and not proof**, and what would constitute proof.

---

### The collapse drill

1. State what the naive solution tracks.
2. State the single number that replaces it.
3. State the property that lets the set collapse, in one sentence.
4. Say what breaks the property.
5. Give the complexity before and after.

### The guard drill

1. Write the reachability loop from memory.
2. Name the one line most people omit.
3. Give an input where omitting it returns the wrong answer.
4. Say why the wrong answer is silent.
5. Say what invariant the guard is really checking.

### The levels drill

1. Explain minimum jumps as a BFS.
2. Name the two variables that stand in for the queue.
3. Say why the levels are contiguous ranges.
4. Give the loop bound and why it is `n - 1`.
5. Say what answer you get with the wrong bound, and on what inputs.

### The variants drill

For each, say what changes and whether greedy survives:

1. Can you reach the end.
2. Fewest jumps to the end.
3. Jumps in both directions.
4. Each landing has a cost.
5. Each landing has a reward.
6. Taps watering a garden.

### The break-it drill

For each, say what happens and whether anything reports it:

1. The guard removed, on `[0, 1]`.
2. The loop running to `n` instead of `n - 1`.
3. Negative jump values.
4. `furthest` initialised to `nums[0]` instead of `0`.
5. Greedy applied when jumps have costs.
6. Greedy applied when jumps go backwards.

---

### The shape drill

1. Say what the scheduler stores and what the only query is.
2. Give the index, and why that index.
3. Say what fraction of the difficulty is scheduling, and what the rest is.
4. Give the average rate at 100M jobs/day.

### The model drill

1. Say why jobs and runs are separate rows.
2. Give the three things that separation buys.
3. Say what drift is and how the model avoids it.
4. Give the unique constraint and what it prevents.
5. Say why the index is partial and what it costs otherwise.

### The claiming drill

1. Say why select-then-update is wrong.
2. Write the atomic claim from memory.
3. Say what `SKIP LOCKED` does and what the throughput is without it.
4. Say why the attempt counter increments on the claim.
5. Say why the subquery is ordered.

### The lease drill

1. Say what a lease is and what expiry means.
2. Give the short-lease failure and the long-lease failure.
3. State why no setting avoids both.
4. Give the heartbeat resolution with concrete numbers.
5. Say what the heartbeat must check, and what happens without that check.
6. Compute the heartbeat write load for 700 workers.

### The guarantee drill

1. Say why exactly-once is not available, in two sentences.
2. Give both honest options and where the `complete` call sits in each.
3. Say what an idempotency key is derived from, and why not per attempt.
4. Give the duplicate rate and the daily count at 100M runs.
5. Say what durable execution changes, and what it costs.

### The herd drill

1. Give the average rate and the instantaneous rate at 09:00.
2. Say why the average being fine is irrelevant.
3. Give the jitter fix and the arithmetic after applying it.
4. Say why jitter defaults to zero, and what risk that creates.
5. Say what rate-limited dispatch adds.
6. Say why catch-up is the same problem wearing a different hat.

### The operations drill

1. Compute daily and 90-day storage.
2. Say why a `DELETE` over that table fails.
3. Give the alternative.
4. Say where the machines actually are, and size the fleet at peak.
5. Say what question you would ask before designing anything, and why.
6. Say when this is the wrong system entirely.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Can you reach the end of the array?*
   The collapse and the property that permits it, the guard and what it catches, and the complexity before and
   after.

2. *Now give me the fewest jumps.*
   That it is a BFS over contiguous levels, which two variables are the queue, the loop bound and what the
   wrong bound gives, and what breaks greedy.

3. *Design a distributed job scheduler.*
   That scheduling is the easy part, `SKIP LOCKED`, the lease trade with no good setting and why, that
   exactly-once is unavailable, and the thundering herd.

---

## Before you move on

- [ ] I can name the single number the reachability solution carries.
- [ ] I can state the property that lets the reachable set collapse to one number.
- [ ] I can say what breaks that property.
- [ ] I write the guard, and I know what it catches.
- [ ] I know the guard's absence is silent on most inputs.
- [ ] I can write reachability from memory in five lines.
- [ ] I can explain minimum jumps as a BFS over levels.
- [ ] I can name the two variables that replace the queue.
- [ ] I know the loop bound is `n - 1`, and what the wrong bound returns.
- [ ] I know the wrong bound is right on some inputs, which is why it survives testing.
- [ ] I can construct an input where costed jumps break greedy.
- [ ] I know Jump Game III needs a real search, and why.
- [ ] I can translate the taps problem into a jump array.
- [ ] I checked the greedy against an `O(n^2)` DP and know why that is evidence, not proof.
- [ ] I can say what the scheduler stores and what the only query is.
- [ ] I know jobs and runs are separate, and the three things that buys.
- [ ] I can give the unique constraint and what it prevents.
- [ ] I know why the index is partial.
- [ ] I can write the atomic claim and explain `SKIP LOCKED`.
- [ ] I know the throughput without `SKIP LOCKED` is one worker's.
- [ ] I know why the attempt counter increments on the claim.
- [ ] I can give both lease failure modes and why no setting avoids both.
- [ ] I can give the heartbeat resolution with numbers.
- [ ] I know the heartbeat must check ownership, and what breaks without it.
- [ ] I can say in two sentences why exactly-once is not available.
- [ ] I know both honest guarantees and where the `complete` call sits in each.
- [ ] I know the idempotency key comes from `(job_id, run_at)`, not per attempt.
- [ ] I can give the duplicate rate and the daily count.
- [ ] I can give the herd arithmetic before and after jitter.
- [ ] I know jitter defaults to zero and what risk that creates.
- [ ] I know why a `DELETE` fails and what replaces it.
- [ ] I know when this is a workflow engine and not a scheduler.
- [ ] I answered all three questions above out loud.
