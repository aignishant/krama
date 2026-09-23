---
day: 166
track: practice
title: "Practice — Interval scheduling"
status: written
---

# Day 166 · Practice

**DSA topic:** Interval scheduling
**System design topic:** Design search autocomplete at scale

---

## Code these, in this order

One rule for the whole set: **before writing anything, say which of the three techniques this is and what the
sort key is.** Greedy selection sorts by end, merging sorts by start, the sweep line sorts the endpoints — and
picking the wrong one gives a plausible number at the same complexity with no error.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Merge Intervals | LeetCode 56 (Medium) | Sort by start, and `max` on the extension. |
| 2 | Insert Interval | LeetCode 57 (Medium) | Whether you notice the input is already sorted. |
| 3 | Non-overlapping Intervals | LeetCode 435 (Medium) | Sort by end, and that it is a subtraction. |
| 4 | Meeting Rooms II | LeetCode 253 (Medium) | The sweep line, and the tie-break at equal times. |
| 5 | Minimum Number of Arrows | LeetCode 452 (Medium) | The same greedy in disguise. |
| 6 | Maximum Profit in Job Scheduling | LeetCode 1235 (Hard) | Weighted — greedy fails, DP with a binary search. |

### On all six, classify before coding

For each, write down: **which technique, which sort key, and what the boundary convention is.** Then solve it.
**Then check whether your classification was right** — and if it was not, say which question you thought you
were answering.

### On problem 1, extend with `= end`

Replace `max(current_end, end)` with `= end`. Run on `[(1,10),(2,3),(11,12)]` and record the output. **Say what
shape of input triggers it**, and why that shape is rare in hand-written tests.

### On problem 1, sort by end instead

Run the merge with the wrong key on the same input. **Record the output and say precisely what went wrong** —
which part of which interval was lost, and why there is no code path that could recover it.

### On problem 2, sort the input

Solve it by appending the new interval and re-sorting. Confirm it gives the right answer. **Then say what it
costs and what the problem was actually testing**, and write the three-phase `O(n)` version.

### On problem 3, notice the subtraction

Before coding, say in one sentence how "minimum removals" relates to "maximum kept". **Then write one function
and derive the other.**

### On problem 4, get the tie-break wrong

Encode the events so that starts sort before ends at equal times. Run on `[(1,4),(4,6),(6,9)]` and record the
answer against 1. **Say why `(time, delta)` tuples give the right convention for free**, and what would happen
if you encoded the events as strings.

### On problem 4, produce the assignment

Extend your solution to say which meeting goes in which room. **Say why the sweep line cannot do this** and
what structure you need instead.

### On problem 6, watch greedy fail

Write the greedy — sort by end, take anything compatible, sum the values — and run it against the DP on
`[(0,10,100),(0,3,10),(3,6,10),(6,9,10)]`. Record both. **Then replace the binary search with a linear scan**
and say what the complexity becomes and at what `n` it stops finishing.

### Then the classification drill

For each of these, name the technique and the sort key without solving it:

1. Maximum number of non-overlapping intervals.
2. Merge overlapping intervals.
3. Minimum meeting rooms.
4. Do any two intervals overlap?
5. Insert into a sorted disjoint list.
6. Maximum total value of non-overlapping intervals.
7. The busiest minute of the day.
8. Minimum removals to make the set disjoint.

**Three are greedy, three are merging, and two are neither.** Say which.

### Then the boundary drill

For each, state whether `[2,4]` and `[4,6]` conflict, and what comparison you would write:

1. Meeting rooms.
2. Non-overlapping meeting selection.
3. Two inclusive number ranges.
4. Two half-open time slots.

---

### The classification drill

1. Give the three techniques and the question each answers.
2. Give the sort key for each and the invariant it establishes.
3. Say what happens when you use the wrong key — for both directions.
4. Say why there is no performance signal warning you.

### The selection drill

1. Give the algorithm in four lines.
2. Give the exchange argument for the end-time sort.
3. Say why start time fails, with an input.
4. Say why duration fails, and why it is the more dangerous wrong key.
5. Give the one-line relationship to "minimum removals".

### The merging drill

1. Give the algorithm.
2. Say what invariant sorting by start establishes.
3. Give the line people get wrong and the input that catches it.
4. Say what the wrong sort key does to the output.

### The sweep drill

1. Describe the decomposition in one sentence.
2. Say what you deliberately stop caring about.
3. Give the tie-break rule and why.
4. Say why `(time, delta)` sorting gets it right for free.
5. Give the two-pointer form and say whether it differs.
6. Say what the sweep cannot answer, and what does.

### The weighted drill

1. Give the counter-example that breaks greedy.
2. Give the DP recurrence.
3. Say what `p(i)` is and how it is found.
4. Say what a linear scan for `p(i)` costs.
5. Give the complexity, and compare it with the greedy version.
6. Say what one word in the problem statement signals this.

### The break-it drill

For each, say what happens and whether anything reports it:

1. Selection sorted by start.
2. Merging sorted by end.
3. `= end` instead of `max` when merging.
4. Starts before ends at equal times in the sweep.
5. Re-sorting an already-sorted input.
6. Greedy on the weighted version.
7. A linear scan for `p(i)`.
8. `.sort()` on the caller's list.

---

### The budget drill

1. Give the latency budget, itemised.
2. Say how much is left for the server.
3. Say why a late suggestion is worse than none.
4. Say what a TLS handshake would do to the budget.

### The traffic drill

1. Compute autocomplete requests from searches per day.
2. Say what the ratio to search traffic is, and why.
3. Give the three client-side reductions and the factor for each.
4. Compute what reaches origin after all three.

### The precomputation drill

1. Say what the obvious design does and why it does not fit.
2. Describe the precomputed structure.
3. Say what the request becomes.
4. Say what the cost is, and what closes the gap.

### The structure drill

1. Give the size of a plain trie at a billion queries, and why.
2. Name the two compressed forms and roughly what each saves.
3. Say why a flat hash map is often the right answer.
4. Say why prefixes are capped, and at roughly what length.

### The layers drill

1. Give both layers with their sizes and update frequencies.
2. Say why they cannot be one structure.
3. Describe the trending layer's storage shape.
4. Say why it is per region.

### The ranking drill

1. Name five signals.
2. Say why frequency goes through a logarithm.
3. Say which server-side signal is strongest, and what it measures.
4. Say which signal is strongest overall and where it can live.
5. Say what on-device personalisation cannot do.

### The delivery drill

1. Say where the time actually goes.
2. Give the client-side filtering guard and why it is needed.
3. Say what a cancellable request prevents.
4. Compute the size of the edge-cacheable head.

### The safety drill

1. Say why filtering is not optional here.
2. Say why it runs at serve time as well as build time.
3. State the asymmetry and which way it points.
4. Compute how cheap the trending layer is to attack.
5. Give the mitigation, and say what it is not.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Merge these intervals — and then, how many meeting rooms do I need?*
   The two techniques, both sort keys and the invariant each establishes, the `max` on the extension, and the
   sweep tie-break.

2. *Now each interval has a value.*
   Why greedy fails with the counter-example, the DP recurrence, what `p(i)` is and why it is a binary search,
   and why the complexity is unchanged.

3. *Design search autocomplete.*
   The latency budget and the per-keystroke traffic, precomputation instead of search, the two layers, and
   where the delivery wins actually are.

---

## Before you move on

- [ ] I classify before coding: which technique, which sort key.
- [ ] I know selection sorts by end, and the exchange argument for it.
- [ ] I know merging sorts by start, and what invariant that gives.
- [ ] I know the sweep sorts endpoints and discards the association.
- [ ] I know what the wrong sort key does in both directions.
- [ ] I know there is no performance signal to warn me.
- [ ] I write `max(current_end, end)` and know the input that catches `= end`.
- [ ] I know "minimum removals" is the same problem, subtracted.
- [ ] I settle the boundary convention before coding.
- [ ] I know `(time, delta)` sorting gives the right tie-break free.
- [ ] I know the sweep counts and a heap assigns.
- [ ] I know the two-pointer form is the same algorithm.
- [ ] I do not re-sort an already-sorted input.
- [ ] I know the weighted counter-example and both numbers.
- [ ] I can give the weighted DP recurrence.
- [ ] I know `p(i)` is a binary search and what a linear scan costs.
- [ ] I know weighted DP is the same `O(n log n)` as the greedy.
- [ ] I know "number" versus "value" is the signal.
- [ ] I can give the autocomplete latency budget, itemised.
- [ ] I know autocomplete traffic is ~15× search traffic, and why.
- [ ] I know why precomputation replaces search, and what it costs.
- [ ] I can describe both layers and their sizes.
- [ ] I know a plain trie is ~1 TB and why.
- [ ] I can name the compressed forms and what they save.
- [ ] I know why prefixes are capped.
- [ ] I can name five ranking signals and which is strongest.
- [ ] I know on-device personalisation is free and what it cannot do.
- [ ] I know the three client-side reductions and their combined factor.
- [ ] I know the client-filtering guard and what a cancellable request prevents.
- [ ] I know why filtering runs at serve time too, and which way the asymmetry points.
- [ ] I answered all three questions above out loud.
