---
day: 167
track: practice
title: "Practice — Merging intervals"
status: written
---

# Day 167 · Practice

**DSA topic:** Merging intervals
**System design topic:** Design a leaderboard

---

## Code these, in this order

One rule for the whole set: **say "further of the two, not the new one" out loud as you write the extension
line.** It is the bug of the day, it passes typical tests, and saying it is the only reliable defence.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Merge Intervals | LeetCode 56 (Medium) | The core loop, and the `max` on the extension. |
| 2 | Insert Interval | LeetCode 57 (Medium) | Whether you re-sort a sorted input. |
| 3 | Interval List Intersections | LeetCode 986 (Medium) | Two pointers, and which one to advance. |
| 4 | Employee Free Time | LeetCode 759 (Hard) | The complement, and its two boundary cases. |
| 5 | Data Stream as Disjoint Intervals | LeetCode 352 (Hard) | Streaming, and multi-block absorption. |
| 6 | Remove Covered Intervals | LeetCode 1288 (Medium) | Containment as the subject rather than the bug. |

### On problem 1, write the bug first

Implement the loop with `current_end = end`. Run on `[(1,3),(2,6),(8,10)]` — the typical test — and record the
output. **Then run it on `[(1,10),(2,3),(11,12)]`** and record that.

**One passes and one does not.** Say why the failing shape is rare in tests and common in real data.

### On problem 1, sort by end

Run the merge with the wrong sort key on `[(1,10),(2,3),(11,12)]`. **Record the output and say exactly what was
lost** — which field of which interval, and why no later step could recover it. **Then say why the block count
being right makes it worse.**

### On problem 1, use tuples

Build `merged` as a list of tuples and try to extend the last one. **Record the exact error.** Say why this is
the friendliest bug of the day.

### On problem 2, count the operations

Solve it by appending and re-sorting. Then write the three-phase version. **Count the operations each performs
on a thousand-interval input** and say what the problem was testing.

### On problem 3, advance the wrong pointer

Always advance `i`. Run it and record the answer. **Then say why advancing whichever ends first is correct**, in
one sentence about what that interval can still intersect.

### On problem 4, drop the bounds

Write `free_time` without a lower and upper bound. **Say what the answer is before the first busy block and
after the last**, and why the question has no answer at the edges without them.

Then add the bounds, and **deliberately pass a lower bound that falls inside the data.** Say what
`cursor = end` does that `cursor = max(cursor, end)` does not.

### On problem 5, absorb only the neighbour

Write the streaming version so that a new interval merges with at most one existing block. Add `(1,3)`,
`(8,10)`, `(15,18)`, then `(4,16)`. **Record the structure after each.** Say what is now wrong and why it
compounds.

### Then the variants drill

Implement all five variants from one merge function. **Time each on a hundred-thousand-interval input** and
record which are `O(n)` and which are `O(n log n)`, and why.

### Then the verification drill

Write a brute force that merges by marking a small number line, and check your merge against it on five hundred
random inputs. **Note which boundary convention the brute force implies**, and make sure you compare against
the matching version.

---

### The algorithm drill

1. Give the loop in four lines.
2. State the invariant that sorting by start establishes.
3. Say why a closed block never reopens.
4. Give the extension line and Hemalatha's six words.

### The bug drill

1. Give the input that catches `= end` and both outputs.
2. Give the input where it is invisible, and both outputs.
3. Say why containment is rare in tests and common in real data.
4. Give the wrong-sort-key output and say what was lost.
5. Say why the correct block count makes that one worse.

### The convention drill

1. Say what `<=` and `<` each mean for `[1,3]` and `[3,5]`.
2. Say which LeetCode uses.
3. Say what you do when the statement does not say.

### The variants drill

For each: the technique, the complexity, and the specific trap.

1. Insert into a sorted disjoint list.
2. The gaps.
3. Intersect two lists.
4. Total covered length.
5. Streaming arrivals.

### The streaming drill

1. Say why the one-pass algorithm does not apply.
2. Give the cost of re-sorting on every arrival.
3. Describe the structure and the two steps per insert.
4. Give the per-insert and the amortised cost.
5. Say why the amortisation works.
6. Give the case that a nearest-neighbour merge gets wrong.

### The break-it drill

For each, say what happens and whether anything reports it:

1. `= end` on a contained interval.
2. Sorting by end.
3. Forgetting the final flush in the two-variable version.
4. Extending a tuple.
5. Re-sorting a sorted input.
6. `cursor = end` in the gaps.
7. Nearest-neighbour-only merging in the stream.

---

### The asymmetry drill

1. Give the two questions and their costs.
2. Say which one almost every naive design fails.
3. Say why that is the opening move.

### The structure drill

1. Name the two structures inside a sorted set.
2. Say what each is for.
3. Say what the spans are and why they matter.
4. Give the four operations and their complexities.
5. Give bytes per entry and size it at 50 million.
6. Give the per-operation latency and the instance utilisation.

### The sharding drill

1. Say why rank cannot be sharded usefully.
2. Give the cost of a sharded rank query.
3. Say why it gets worse with more shards.
4. Give the three alternatives.
5. Say which you would take, and why it is a product fact.

### The approximation drill

1. Describe the histogram and its size.
2. Give the ratio against the exact structure.
3. Say where exact is required and where it is not.
4. Give the sentence that justifies it as a product decision.
5. Say what the interface must show.

### The ties drill

1. Say what Redis does by default and why that is worse than random.
2. Give the composite-score formula.
3. State the precision bound and what exceeding it does.
4. Say what must never reach the screen.
5. Say why an application-level tie-break cannot work for rank.

### The windows drill

1. Give the three or four windows and their TTLs.
2. Compute the write amplification.
3. Say why that trade is right.
4. Say which sharding is easy here, and why.
5. Say what is genuinely hard about a rolling window, and the honest answer.

### The durability drill

1. Say what is the source of truth and what is not.
2. Give the write ordering and what the other ordering loses.
3. Describe the rebuild, including the atomic step.
4. Give the rebuild time and say why it is acceptable here.
5. Say what kind of system it would not be acceptable for.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Merge these intervals.*
   The sort key and the invariant it gives, the loop, the extension line with its bug, the boundary
   convention, and the complexity.

2. *What if they arrive one at a time?*
   Why the single pass does not apply, the structure, the two steps per insert, multi-block absorption, and
   the amortised cost with its reason.

3. *Design a leaderboard.*
   The top-ten versus rank asymmetry, the skip list with its spans, the sizing, why rank cannot be sharded,
   and exact-at-the-top with approximate below.

---

## Before you move on

- [ ] I sort by start and can state the invariant it gives.
- [ ] I say "further of the two, not the new one" while writing the extension.
- [ ] I know the input that catches `= end` and the one where it is invisible.
- [ ] I know why containment is rare in tests and common in real data.
- [ ] I know what sorting by end loses, and why the block count stays right.
- [ ] I settle the boundary convention, and ask when it is unstated.
- [ ] I build with lists or two variables, never by extending a tuple.
- [ ] I remember the final flush in the two-variable version.
- [ ] I do not re-sort an already-sorted input.
- [ ] I can write insert as three phases.
- [ ] I know the gaps need explicit bounds and why.
- [ ] I know `cursor = max(cursor, end)` and what it guards against.
- [ ] I can intersect two lists and say which pointer to advance, and why.
- [ ] I know why merging first is required before summing coverage.
- [ ] I know the single pass does not apply to a stream.
- [ ] I can describe the streaming structure and its two steps.
- [ ] I know one arrival can absorb several blocks.
- [ ] I can give the amortised cost and explain why it holds.
- [ ] I open a leaderboard answer with the top-ten versus rank asymmetry.
- [ ] I can name both structures inside a sorted set and what each does.
- [ ] I can explain the spans and why they make rank logarithmic.
- [ ] I can size it: bytes per entry, total, and instance utilisation.
- [ ] I know rank cannot be usefully sharded, and why it gets worse.
- [ ] I can give the three alternatives and pick one.
- [ ] I know the histogram size and the ratio against exact.
- [ ] I can justify approximation as a product decision, not a fallback.
- [ ] I know the default tie-break and why it is worse than random.
- [ ] I can give the composite score and its precision bound.
- [ ] I know the window TTL design and the write amplification.
- [ ] I know Redis is the serving structure, and the rebuild path.
- [ ] I answered all three questions above out loud.
