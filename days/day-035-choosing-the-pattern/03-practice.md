---
day: 35
track: practice
title: "Practice — Choosing between two pointers and a window, under pressure"
status: written
---

# Day 035 · Practice

**DSA topic:** Choosing between two pointers and a window, under pressure
**System design topic:** Locking and deadlocks

**Theme:** Worker pools and pipelines

---

## Code these, in this order

Four problems chosen so that the route is the work. **For each one, run the checklist out loud and
name the room before writing anything** — Q1 contiguous? Q2 fixed k? Q3 best or count? Q4 monotonic?
Q5 which pointer shape? Time the routing: under a minute each.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Merge Sorted Array | LeetCode 88 (Easy) | Routing to pointers, then the real lesson: overlapping destination → write from the back. |
| 2 | Backspace String Compare | LeetCode 844 (Easy) | First route (stack) versus the follow-up route (two pointers, backwards, O(1) space). |
| 3 | Longest Subarray of 1's After Deleting One Element | LeetCode 1493 (Medium) | Window, maximise shape, collapsed map — and the `right - left` twist for the forced deletion. |
| 4 | Maximum Sum of Distinct Subarrays of Length K | LeetCode 2461 (Medium) | Hearing "length k" over "distinct": fixed window carrying a sum and a map together. |

### On problem 1, break it twice

Write it correctly, from the back. Then write the front-first version on
`([1,2,3,0,0,0], 3, [2,5,6], 3)` and watch the 3 disappear: `[1,2,2,5,6,0]`. Say the rule —
overlapping source and destination, write from the free end.

Then drop the `i >= 0` guard and run `([2,0], 1, [1], 1)`. You get `[2,2]`, no crash. Say why
`nums1[-1]` did not raise, and which earlier day warned you about it.

### On problem 2, do both routes

Stack version first — and feed it `"##a"` before you guard the pop, so you have seen
`IndexError: pop from empty list` once on purpose. Then the O(1)-space route: why must the pointer
version walk backwards? Say it in one sentence before writing it — a backspace's effect runs right
to left, so certainty only exists from the back.

### On problem 3, route it aloud first

The full routing sentence before code: contiguous, longest, condition "at most one zero" which is
monotonic, carries one integer. Then the twist: why `right - left` and not `right - left + 1`, and
which input that one character handles for free. Confirm `[1,1,1]` gives 2 and `[1,1,0,1]` gives 3.

### On problem 4, name both parents

This is day 031's shape carrying day 033's map. Say which rule from each day applies — enter/leave
at `i` and `i - k`; `del` at zero because `len(count)` is the test. Confirm
`([1,5,4,2,9,9,9], 3)` gives 15 and `([4,4,4], 3)` gives 0.

### The routing drill

Name the room for each, in under ten seconds, out loud — pattern and day:

1. Longest substring with at most two distinct characters.
2. Given a sorted array, count pairs summing below a target.
3. Remove every occurrence of a value, in place, return the new length.
4. Does this linked list contain a cycle?
5. Count subarrays with exactly three odd numbers.
6. Maximum average of any subarray of length k.
7. Longest increasing subsequence.
8. Two Sum, unsorted, return the indices.
9. Shortest subarray with sum at least k — values may be negative.
10. Reverse the vowels of a string in place.
11. How many subarrays have a product below 100?
12. Find the middle of a linked list in one pass.

Numbers 7, 8 and 9 are the exits — say where each one routes *away* to, and why.

### The abandon drill

For each discovery, say what you do next:

1. Mid-problem, the interviewer confirms elements may be skipped.
2. Mid-problem, you learn the values can be negative and your condition is a sum.
3. Your plan was to sort, and the expected output is a pair of original indices.

### The deadlock-telling drill

Tell the two-transaction transfer story from memory — T1 does 7→42, T2 does 42→7 — with the two
lock acquisitions, the two waits, and the moment the cycle closes. Under a minute, no notes. Then
the one-line distinction: blocking is a queue, deadlock is a cycle.

### The prevention drill

Answer each in one or two sentences, out loud:

1. Why does locking in a consistent order make the cycle impossible?
2. What does the application do when it receives `deadlock detected`?
3. Why must retried transactions be free of side effects?
4. What does `deadlock_timeout` control, and why is raising it the wrong fix?
5. Ten workers, one jobs table — which three words of SQL stop them queueing on one row?
6. When is optimistic locking the better tool, and what column does it need?

### The arithmetic drill

From memory, in under two minutes:

- One row, lock held 100 ms, 100 wanters in one second — throughput through that row, and the last
  waiter's latency.
- Transfers between one account pair at 20/s each way, 10 ms first-lock hold — roughly what fraction
  collide, and what the ordering rule takes that to.
- A genuine deadlock with `deadlock_timeout` at one second — the victim's user-visible cost, all in.

---

## Build these, in all three languages

Complete each exercise in Python, Go, and C++. Use today's lessons as references, then explain the result without looking at them.

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Process twenty numbered jobs on three workers and return squares in input order. | Bounded active work and indexed results. |
| 2 | Make one job slower and show that completion order can differ from result order. | Scheduling versus presentation. |
| 3 | Make job 7 fail and report its identity while ensuring all worker lifetimes end. | Failure collection and graceful shutdown. |

## Compare

- **Python** — ThreadPoolExecutor reuses worker threads and returns futures. ProcessPoolExecutor uses separate processes for work that benefits from parallel CPU execution. After building, say what was easiest and hardest in this version.
- **Go** — A worker pool runs a fixed number of goroutines over a shared jobs channel. Fan-in collects their results through one output channel. After building, say what was easiest and hardest in this version.
- **C++** — A fixed thread pool combines worker threads with a synchronised task queue. Futures connect each submitted task to its eventual value or exception. After building, say what was easiest and hardest in this version.

Python executors provide a pool, Go commonly uses worker goroutines and channels, and C++ can build a pool from threads plus a protected queue. Returning every result still needs storage proportional to the result set.

For each implementation, state the expected output, the input that exposes a mistake, and the time and extra space used.

## Say these out loud

### DSA and system design

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *You have thirty seconds. What pattern does this problem want: "longest run of 1s if you may flip
   at most two 0s"?*
   Run the checklist audibly — contiguous, variable, maximise, monotonic, carries one integer — and
   finish with the shape sentence: shrink while invalid, record after.

2. *What is a deadlock, and how would you prevent one?*
   The two-transfer story, queue against cycle, detection and the victim, then the ordering rule by
   name — plus short transactions and `lock_timeout` as the supporting habits.

3. *How would you build a job queue on Postgres?*
   `FOR UPDATE SKIP LOCKED`, why workers stop colliding, and what happens to a crashed worker's job
   — then the honest sentence about when this pattern runs out and a real broker earns its place.

### Languages

1. How would you process a million items with eight workers?
2. Does max_workers bound every queued job? Compare the answer across all three languages.
3. What happens if a collector returns early? Explain the corresponding design decision in Python and C++.

## Before you move on

- [ ] I run the five routing questions out loud before writing any code, in under a minute.
- [ ] I can name the three exits — subsequence, indices-plus-sorting, negatives-in-a-sum — and where
      each routes to.
- [ ] I write from the free end whenever source and destination overlap, and I guard indices that
      can go negative.
- [ ] I can tell the deadlock story with both timelines and say why it is a cycle, not a queue.
- [ ] I can state the ordering rule and put it inside a query with `ORDER BY id FOR UPDATE`.
- [ ] I know what the application does on `deadlock detected`, and why retries must be
      side-effect-free.
- [ ] I answered the DSA, system design, and language questions out loud.
- [ ] I completed all three language exercises in Python, Go, and C++.
- [ ] I can predict the examples and explain the failure cases.
