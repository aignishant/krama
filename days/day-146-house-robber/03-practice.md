---
day: 146
track: practice
title: "Practice — House robber and the choice at each step"
status: written
---

# Day 146 · Practice

**DSA topic:** House robber and the choice at each step
**System design topic:** Design a URL shortener

---

## Code these, in this order

One rule for the whole set: **before writing the recurrence, write down the two branches as English.** "If I
take this, then ___ is forbidden, so I add to ___. If I skip it, ___." Every problem below is the same two
branches with different forbidding.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | House Robber | LeetCode 198 (Medium) | The take-or-skip recurrence and `dp[1] = max(m[0], m[1])`. |
| 2 | House Robber II | LeetCode 213 (Medium) | The circle, the two runs, and the `n == 1` guard. |
| 3 | Delete and Earn | LeetCode 740 (Medium) | Index by value — then it *is* problem 1. |
| 4 | Best Time to Buy and Sell Stock with Cooldown | LeetCode 309 (Medium) | The same forbidding, expressed as three states per day. |
| 5 | House Robber III | LeetCode 337 (Medium) | The same choice, on a tree instead of a line. |
| 6 | Maximum Sum with No Three Consecutive | — | A window of three; write it from the pattern. |

### On problem 1, write both wrong answers first

Implement greedy-by-value and alternating-indices. Run all three on `[900, 1600, 900]` and `[2, 1, 1, 2]`.
Record six numbers. **Keep those two arrays** — they are the counter-examples you produce in the interview.

### On problem 1, get `dp[1]` wrong on purpose

Set it to `money[1]` and run on `[5, 1, 5]`. Record the answer. Then write the state sentence above the line
and see that the sentence and the code disagree.

### On problem 2, break the guard

Run your circular version on `[5]` without the `n == 1` guard. Record what it returns. Then explain in one
sentence why both slices are empty.

### On problem 3, find the sizing trap

Run it on `[1, 1000000]` and record the size of the `earnings` array. Then say what the complexity actually is,
in terms of which variable. Then sketch the sorted-distinct-values version and say what it costs instead.

### On problem 5, notice what stays and what changes

The tree version has the same choice — take this node and its grandchildren are next, or skip it and take its
children. Write the two branches as English before coding. Then say what replaced "index `i-2`".

### Then the reconstruction drill

Add `which houses` to problem 1. Do it once by walking the table backwards and once with an explicit
took/skipped array. Then run the space-optimised version and confirm you cannot answer the question at all.

---

### The choice drill

1. State the two branches in English, for house robber.
2. Do the same for delete-and-earn, cooldown and the tree version.
3. Say what the "forbidding" is in each, and how far back it reaches.
4. Say what the tell is for this family in a problem that never says "adjacent".

### The greedy-trap drill

1. Give the greedy-by-value counter-example and both totals.
2. Give the alternating counter-example and both totals.
3. Say in one sentence why no smarter greedy rule fixes it.
4. Say why "non-adjacent" and "alternating" are different.

### The base-case drill

1. Give `dp[0]` and `dp[1]` and justify each from the state sentence.
2. Say what `dp[1] = money[1]` produces on `[5, 1, 5]`.
3. Say why the two-variable version needs no guards at all.

### The circular drill

1. State the two runs and what each excludes.
2. Give both halves of the correctness argument.
3. Say why a single pass cannot enforce the constraint.
4. Give the input that breaks it without a guard.

### The variations drill

1. Extend to a forbidden window of width `w`: the recurrence, the base cases, the space window.
2. Say why widening `w` does not make it harder.
3. Say what kind of forbidding rule *would* make it harder, with an example.

### The costs drill

1. Give time and space for all five variants.
2. Give delete-and-earn's complexity and name the variable that is not `n`.
3. Compare against trying every subset, at `n = 30`.
4. Say why greedy is not even faster than the DP.

### The break-it drill

Trigger each and record the exact output or error:

1. Greedy by value on `[900, 1600, 900]`.
2. Alternating indices on `[2, 1, 1, 2]`.
3. `dp[1] = money[1]` on `[5, 1, 5]`.
4. The table version on a one-element input.
5. The circular version on `[5]` with no guard.
6. `earnings` sized by `len(nums)` instead of `max(nums)`.
7. Asking which houses were robbed, from the two-variable version.

---

### The requirements drill

1. Give the in-scope and out-of-scope lists you would state.
2. Give the three non-functional requirements and why each matters here.
3. Say why "the redirect is on somebody else's critical path" changes the design.

### The estimation drill

1. Do the full sizing from 100M URLs a month: writes, peak, reads, storage per year and per five years.
2. Say the decision sentence that follows.
3. Say what a candidate who starts sharding has missed.

### The code-generation drill

1. Name the three schemes and reject two, with reasons.
2. Describe block allocation and compute the coordination rate at 200 writes/s.
3. Say what a server crash costs, and why that is acceptable.
4. Explain the scrambling multiply and state plainly what it is and is not.
5. Give the length arithmetic for 5, 6 and 7 characters.
6. Say why base 62 and not 64, and when you would use 58.

### The redirect drill

1. Give the read path, step by step, with latencies.
2. Say where the click event goes and why it is not awaited.
3. Say what negative caching prevents.
4. Give the cache sizing for 10M hot entries and the expected hit rate.
5. Say what invalidation is needed and what forces it.

### The 301/302 drill

1. State what each one does to the browser.
2. Give what you gain and lose with each — two each.
3. Say which a commercial shortener uses and why.
4. Say which an internal one might use and why.
5. Say how this interacts with the abuse response.

### The abuse drill

1. Name the five defences in order.
2. Say which one people forget, and why it matters.
3. Say why `is_disabled` rather than deleting.
4. Say what redirect targets you would block outright.
5. Say what abuse prevention forces on the caching design.

### The numbers drill

1. Storage per row, per month, per year, over five years.
2. Code space for lengths 5, 6, 7, and years of runway at 100M/month.
3. Collision probability for random 7-character codes after 10M and 100M issued.
4. Cache memory for 10M entries, and database load at 95% and 50% hit rates.
5. Latency budget for a cache hit and a miss.
6. Analytics volume: raw events per day and per year, against hourly aggregates.
7. The traffic reduction 301 buys, and what it costs.

### The failure drill

For each, say what happens and what you would build:

1. The central counter service is unavailable for ten minutes.
2. An application server restarts mid-block.
3. A link gets a million clicks in an hour.
4. A bot probes a million random codes.
5. A link is disabled but was served as a 301 last week.
6. A custom alias request for `/admin`.
7. The click-event queue is down.

Two of the seven are invisible to users by design. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Maximise the sum with no two adjacent elements.*
   The two branches as English, the recurrence, the state sentence and the base case it forces, both
   counter-examples with their numbers, and the space collapse.

2. *Now the houses are in a circle.*
   The two runs, both halves of the correctness argument, why a single pass cannot work, and the `n == 1`
   guard.

3. *Design a URL shortener.*
   The scope, the sizing ending in "this fits on one machine", code generation with block allocation and the
   length arithmetic, the redirect path with the click event off it, and 301-versus-302 named as a product
   decision.

---

## Before you move on

- [ ] I write the two branches as English before the recurrence.
- [ ] I can give the take-or-skip recurrence from the choice.
- [ ] I know `dp[i]` means "considering houses 0..i" and what that forces for `dp[1]`.
- [ ] I have both counter-examples memorised with their numbers.
- [ ] I can say why no greedy rule fixes it.
- [ ] I know non-adjacent is not alternating.
- [ ] I can give the circular two-run trick and both halves of its correctness.
- [ ] I know the `n == 1` guard and why it is needed.
- [ ] I know the two-variable version needs no guards.
- [ ] I can extend to a window of width `w` and say why it is no harder.
- [ ] I know what kind of forbidding rule *would* be harder.
- [ ] I can do the delete-and-earn transformation and name its real complexity variable.
- [ ] I know reconstruction and space optimisation are mutually exclusive.
- [ ] I do the URL shortener sizing before anything else.
- [ ] I can say the decision sentence that follows from it.
- [ ] I can reject two code-generation schemes with reasons.
- [ ] I can describe block allocation and compute its coordination rate.
- [ ] I can give the length arithmetic and justify six or seven characters.
- [ ] I know why base 62, and when 58.
- [ ] I know the click event goes on a queue and is not awaited.
- [ ] I know what negative caching prevents.
- [ ] I can state the 301/302 trade with what each gains and loses.
- [ ] I know why a commercial shortener uses 302.
- [ ] I can name five abuse defences and the one people forget.
- [ ] I know why `is_disabled` rather than deleting.
- [ ] I know what abuse prevention forces on caching.
- [ ] I can give the analytics volume both ways.
- [ ] I answered all three questions above out loud.
