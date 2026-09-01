---
day: 144
track: practice
title: "Practice — Fibonacci: memoisation versus tabulation"
status: written
---

# Day 144 · Practice

**DSA topic:** Fibonacci: memoisation versus tabulation
**System design topic:** Building blocks revision and interview questions

---

## Code these, in this order

One rule for the whole set: **solve each one three times — memoised, tabulated, space-optimised — and do the
conversion by the five steps rather than by rewriting from scratch.** The conversion is a procedure, and the
point of today is to make it automatic.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Fibonacci Number | LeetCode 509 (Easy) | The five conversion steps, on the simplest possible case. |
| 2 | Climbing Stairs | LeetCode 70 (Easy) | Same shape, different base cases. |
| 3 | Min Cost Climbing Stairs | LeetCode 746 (Easy) | Where the answer lives — `min(dp[n-1], dp[n-2])`, not `dp[n-1]`. |
| 4 | Unique Paths | LeetCode 62 (Medium) | Two dimensions; the one-row collapse and its direction. |
| 5 | House Robber | LeetCode 198 (Medium) | A real choice per step, and the two-variable window. |
| 6 | Delete and Earn | LeetCode 740 (Medium) | Transform the input first, then it *is* House Robber. |

### On problem 1, do the conversion out loud

Write the memoised version, then say each of the five steps aloud as you apply it. Parameter to index. Base
cases to initial values. Calls to reads. Loop order — and say which direction the recursion goes and therefore
which way the loop runs. Return the cell.

Then write the loop backwards on purpose and record what it returns.

### On problem 1, find where top-down dies

Call the memoised version with increasing `n` until it raises. Record the value. Then call the tabulated
version with `n = 5000` and confirm it is instant. Then try `sys.setrecursionlimit(1_000_000)` and the memoised
version again, and record what you get instead of a `RecursionError`.

### On problem 4, get the one-row direction wrong

Solve it with a full 2D table, then collapse to one row going left to right, then try right to left. Record
all three answers for a 3 × 3 grid. Write one sentence saying which value each read is supposed to be, and
why only one direction delivers both.

### On problem 5, ask for the path

After solving it, return *which houses* were robbed, not just the total. Do it once from the full table by
walking backwards, and once with parent pointers. Then say what the space-optimised version can and cannot
answer.

### Then the sparse-state experiment

Write coin change with denominations `[1000, 5000]` and amount `100000`, both ways. Instrument:

1. How many cells the bottom-up table fills.
2. How many states the memoised version actually visits (`cache_info().currsize`).

Two numbers, and the ratio is the argument for top-down that nobody expects.

---

### The conversion drill

1. Recite the five steps in order.
2. State the loop-order rule in one sentence.
3. Convert Fibonacci by the steps, out loud, without looking.
4. Convert unique paths the same way, and say why both loops go upwards.
5. Say what step 4 costs you if you get it wrong — the symptom, not the fix.

### The two-forms drill

1. Say what each form is, in one sentence each.
2. Say what is identical between them and what is not.
3. Give the two reasons to convert to bottom-up.
4. Give the one reason to stay top-down, with an example.
5. Say why memoisation does not save you from the recursion limit.

### The space drill

1. State the window rule.
2. Give the window for `dp[i-1], dp[i-2]`; for all of row `i-1`; for rows `i-1` and `i`.
3. Say why the simultaneous assignment matters, and what you get without it.
4. Say why the one-row iteration direction is part of the correctness.
5. Say what optimising costs you, and what to ask before doing it.

### The costs drill

1. Give the time formula and say why both forms share it.
2. Give the three space profiles: memoised, tabulated, optimised.
3. Give Python's usable recursion depth and what raising it produces.
4. Give the per-state constant-factor difference between the forms.
5. Compute the sparse coin-change comparison.

### The break-it drill

Trigger each and record the exact output or error:

1. The loop running in the wrong direction.
2. `curr = prev + curr` followed by `prev = curr`.
3. The one-row collapse iterated right to left, on unique paths.
4. The conversion done without writing the base cases.
5. Memoised recursion at `n = 5000`.
6. `sys.setrecursionlimit(1_000_000)` and then the same call.
7. An `lru_cache`d function that reads a mutable global, across two test cases.

Five of the seven give no error. Name them.

---

### The decision-table drill

For each requirement, name the component and the number that decides:

1. "The user should not wait for the confirmation email."
2. "Analytics, fraud and the recommendation team all want signup events."
3. "We need to reprocess last month after fixing a bug."
4. "Find restaurants by name and cuisine, ranked."
5. "Store the uploaded photos."
6. "Dashboards for CPU and request rate."
7. "The business wants revenue by region by month."
8. "The map marker should move as the driver moves."
9. "Tell the user when the app is closed."
10. "Find drivers within two kilometres."
11. "Have we crawled this URL before?"
12. "This is read a thousand times per write."

### The three-questions drill

1. State the three placement questions.
2. Apply all three to: order placement, menu display, driver location, and the analytics dashboard.
3. Say what "does the user need the answer to continue" implies when the answer is no.
4. Say what every derived copy owes the design.

### The switching-points drill

Give the number for each:

1. Postgres full-text search to Elasticsearch.
2. Read replica to a warehouse.
3. Polling to a push channel.
4. A queue to Kafka.
5. Single node to sharded.

### The what-people-get-wrong drill

One sentence each, from memory:

1. Queues.
2. Kafka.
3. Stream processing.
4. Object storage.
5. Search.
6. Time-series.
7. Warehouses.
8. Batch pipelines.
9. Real-time channels.
10. Push notifications.
11. Geospatial.
12. Bloom filters.

### The numbers drill

Quote from memory, then check:

1. The latency ladder, all five rungs.
2. Throughput for Redis, Kafka, Postgres writes, a Postgres hot row, Elasticsearch bulk, Prometheus.
3. Cost per GB for object storage, database SSD, and egress.
4. Compression ratios for time-series, search index, and columnar.
5. Staleness defaults for Elasticsearch refresh, CDC, nightly batch, Kafka retention.

Then compute:

6. Egress versus storage for 40 TB of images.
7. Row versus column scan for a `sum` over 40M rows.
8. Polling versus WebSocket bandwidth for 100,000 users at 5 seconds.
9. Bloom filter versus exact set for a billion URLs.
10. SNS→SQS versus Kafka storage for 5 consumers over 7 days.

### The trade-offs drill

State each as the sentence you would say out loud:

1. Derived copies.
2. Synchronous versus asynchronous.
3. Operational cost of every added component.
4. Exactness versus cost.
5. More real-time than the product needs.

Then list the seven things you would not add, and the trigger that would change each answer.

### The failure drill

For each, say what happens and what you would build:

1. A dual write to the database and the search index, with a crash in between.
2. A read replica used for a full-scan analytics query.
3. A metric labelled with a user id.
4. A push notification carrying the only copy of the message.
5. A WebSocket fleet restarted all at once.
6. A Bloom filter holding five times its design capacity.
7. A Kafka topic keyed by country, where one country is 60% of traffic.

Two of the seven lose data. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Write it top-down. Now write it bottom-up.*
   The memoised version first with the recurrence stated, then the five conversion steps named as you apply
   them, the loop-order rule, and the space collapse with its window.

2. *Your solution crashes on the large input.*
   Recursion depth, why memoisation does not prevent it, the bottom-up conversion as the fix, and why raising
   the limit is worse — plus the alternative check if it is a `MemoryError` instead.

3. *You need search, a queue and a cache. Which technologies, and why?*
   The requirement each answers rather than the product name, the number that decides each, what each costs,
   and the observation that two of the three are derived copies that owe a staleness number and a
   reconciliation job.

---

## Before you move on

- [ ] I can recite the five conversion steps.
- [ ] I know the loop always runs opposite to the recursion.
- [ ] I can convert a 1D and a 2D DP by the steps, out loud.
- [ ] I know what a wrong loop direction produces, and that it is silent.
- [ ] I know the two reasons to convert to bottom-up.
- [ ] I know the one reason to stay top-down, with the sparse-state example.
- [ ] I know memoisation does not prevent the recursion limit, and why.
- [ ] I know what raising the recursion limit produces.
- [ ] I can state the space window rule and apply it in 1D and 2D.
- [ ] I know why the simultaneous assignment matters.
- [ ] I know the one-row direction is part of the correctness.
- [ ] I know what optimising costs and what to ask first.
- [ ] I can place any of the twelve requirements onto a component.
- [ ] I can state the three placement questions and apply them.
- [ ] I know every derived copy owes a staleness number, a sync mechanism and reconciliation.
- [ ] I can give the five switching points with their numbers.
- [ ] I can give the what-people-get-wrong line for all twelve components.
- [ ] I can quote the latency ladder and the throughput figures.
- [ ] I can quote storage and egress costs and compute the 40 TB case.
- [ ] I can compute row versus column, polling versus push, and Bloom versus exact.
- [ ] I can state all five trade-offs as sentences.
- [ ] I can name seven things I would not add, and what would change my mind.
- [ ] I know the burden of proof is on leaving the database.
- [ ] I answered all three questions above out loud.
