---
day: 168
track: practice
title: "Practice — Meeting rooms and the sweep line"
status: written
---

# Day 168 · Practice

**DSA topic:** Meeting rooms and the sweep line
**System design topic:** Design an ad click aggregator

---

## Code these, in this order

One rule for the whole set: **state the tie-break convention before you write the sort.** Does an event ending
at time `t` conflict with one starting at `t`? It is one comparison, the problem decides it, **and getting it
backwards gives an answer exactly one too high on the most realistic inputs there are.**

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Meeting Rooms | LeetCode 252 (Easy) | The opener — and whether you sort at all. |
| 2 | Meeting Rooms II | LeetCode 253 (Medium) | The sweep, and the tie-break. |
| 3 | Car Pooling | LeetCode 1094 (Medium) | A weighted sweep, and dense coordinates. |
| 4 | My Calendar III | LeetCode 732 (Hard) | A sweep over a stream of arrivals. |
| 5 | The Skyline Problem | LeetCode 218 (Hard) | The same sweep with `max` as the accumulator. |
| 6 | Minimum Interval to Include Each Query | LeetCode 1851 (Hard) | A sweep over two sorted streams at once. |

### On problem 2, get the tie-break wrong on purpose

Encode the events so that starts sort before ends at equal times. Run on `[(1,4),(4,6),(6,9)]` and record the
answer against 1. **Then run the correct version.** Say why abutting meetings are the normal case rather than
an edge case.

### On problem 2, encode the events as strings

Use `(time, "start")` and `(time, "end")`. Confirm it gives the right answer. **Then rename them to `"begin"`
and `"finish"` and run it again.** Say what happened and why numbers are the right encoding.

### On problem 2, produce the assignment

Extend your solution to say which meeting is in which room. **Say why the sweep alone cannot do this**, and
check that the heap's size equals the sweep's answer. **If they disagree, find which convention differs.**

### On problem 3, notice the coordinates are dense

The problem caps locations at 1,000. **Write both the sweep and a difference array.** Time both at
`n = 10,000` trips and record the ratio. **Say roughly where the crossover between the two approaches is.**

### On problem 4, notice it is a stream

You cannot sort — bookings arrive one at a time and each must be answered immediately. **Say what changes**,
and implement it with a running count in a sorted map. **Then say what the per-insert cost is.**

### On problem 5, start from the meeting-rooms code

Take your sweep and change only the accumulator. **Write down what the accumulator must support** — add,
remove, report the maximum — and say why a plain heap does not support all three.

Then implement lazy deletion. **Say why it stays `O(n log n)` despite the heap holding stale entries.**

### On problem 6, find the two streams

There are intervals and there are queries, both sortable. **Say what you sweep over and what the accumulator
is.** Then implement it.

### Then the floating-point drill

Build a set of intervals with times like `0.1 + 0.2` and `0.3`. Run your sweep. **Record what happens to the
tie-break** and say why integers are the only safe representation.

### Then the verification drill

Write a brute force that, for every interval's start, counts how many intervals contain that instant. Check
your sweep against it on five hundred random inputs. **Say why checking only at interval starts is
sufficient.**

---

### The decomposition drill

1. State the technique in one sentence.
2. Say what you deliberately discard, and what that buys.
3. Say what question the sweep answers and what it cannot.
4. Give the complexity and what dominates it.

### The tie-break drill

1. Give both conventions and the question each answers.
2. Say which one meeting rooms needs, and why.
3. Say what `(time, delta)` sorting gives you for free, and why.
4. Say why string encoding is a coincidence rather than a design.
5. Say by how much the wrong convention is wrong, and on what input.
6. Say what floating-point times do to it.

### The forms drill

1. Give the event-list form.
2. Give the two-pointer form and say where the tie-break lives in it.
3. Say whether they differ in complexity.
4. Give the heap form and what it adds.
5. Say what consistency check the heap gives you free.

### The variants drill

For each, say what changes and what the accumulator becomes:

1. How many rooms.
2. The busiest moment.
3. Total covered length.
4. Peak bandwidth.
5. The skyline.

### The when-not-to drill

1. Give the condition under which a difference array wins.
2. Compute both costs at 10,000 meetings over 1,440 minutes.
3. Say when the array version becomes absurd.
4. Give the rough crossover rule.
5. Say what two dimensions require instead.

### The break-it drill

For each, say what happens and whether anything reports it:

1. Starts before ends at equal times.
2. Events encoded as `"begin"` and `"finish"`.
3. Applying the delta before accumulating covered time.
4. A difference array over a year in seconds.
5. Floating-point times.
6. Sweep and heap with mismatched conventions.
7. Skyline without lazy deletion.

---

### The shape drill

1. Give events in and queries out, with volumes.
2. Say what the central design move is, and why.
3. Say what nobody ever does, and why that matters.

### The pipeline drill

1. Name the five stages.
2. Say what the ingest endpoint must not do, and why.
3. Say what the queue buys you.
4. Say what partitioning by campaign removes.
5. Say what status code the endpoint returns and why.

### The time drill

1. Give both timestamps and what each is for.
2. Say what bucketing by arrival time gets wrong, in two ways.
3. Say what bucketing by event time costs.
4. Define a watermark and say what it advances with.
5. Say what happens to data past the grace period.
6. Give the lateness distribution and the volume at the tail.
7. State the trade honestly.

### The duplicates drill

1. Name three sources of duplicates.
2. Say where the event id must come from and why.
3. Say why the dedup check must be atomic.
4. Compute exact dedup memory for five minutes and for an hour.
5. Say why a Bloom filter is right for a crawler and wrong here.
6. Give the two-layer resolution.

### The storage drill

1. Compute the full cross-product and say what fraction is zero.
2. Compute the sparse query-driven total.
3. Give the ratio.
4. Say what adding a new dimension costs.
5. Say what that means for when the decision must be made.

### The two-paths drill

1. Give both paths with their properties.
2. Say which serves what.
3. Say which number goes on the invoice.
4. Say what metric you would alert on.
5. Give the standard criticism and your answer to it.

### The honesty drill

1. Say what aggregation is lossy about.
2. Say why the raw log is kept.
3. Say what you approximate and what you count exactly.
4. Say what must be labelled on the dashboard, and why.
5. Say why flagged fraudulent events are stored rather than dropped.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *How many meeting rooms do you need?*
   The decomposition and what it discards, the tie-break with its convention and its cost, the two equivalent
   forms, and what the sweep cannot answer.

2. *Now give me the skyline.*
   That it is the same sweep with a different accumulator, what the accumulator must support, lazy deletion,
   and why it stays `O(n log n)`.

3. *Design an ad click aggregator.*
   Aggregate on the way in, event time versus processing time with watermarks, why a Bloom filter is wrong
   here, the cross-product trap, and the two paths.

---

## Before you move on

- [ ] I can state the sweep in one sentence, including what it discards.
- [ ] I know "how many at once" and "which is which" are different questions.
- [ ] I settle the tie-break before writing the sort.
- [ ] I know `(time, delta)` gives the meeting-rooms convention free, and why.
- [ ] I never encode events as strings.
- [ ] I know the wrong convention is exactly one too high, on abutting inputs.
- [ ] I work in integers, and know what floats do to the tie-break.
- [ ] I can write both the event-list and two-pointer forms.
- [ ] I know the sweep cannot give the assignment, and what can.
- [ ] I know the heap's size agrees with the sweep, and use it as a check.
- [ ] I can do the busiest-moment variant and know `>` versus `>=`.
- [ ] I can do total-covered and know to accumulate before applying the delta.
- [ ] I can do a weighted sweep.
- [ ] I know the skyline is the same sweep with `max` as the accumulator.
- [ ] I can explain lazy deletion and why it stays `O(n log n)`.
- [ ] I know when a difference array beats the sweep, with the arithmetic.
- [ ] I know the rough crossover rule.
- [ ] I can give the ad aggregator's shape: events in, queries out.
- [ ] I know the central move is to aggregate on the way in.
- [ ] I can name the five stages and what the endpoint must not do.
- [ ] I know why partitioning by campaign removes coordination.
- [ ] I know both timestamps and what arrival-time bucketing gets wrong.
- [ ] I can define a watermark and say what it advances with.
- [ ] I know the lateness distribution and the daily volume at the tail.
- [ ] I can name three sources of duplicates.
- [ ] I know where the event id must come from.
- [ ] I can say why a Bloom filter is wrong here and right for a crawler.
- [ ] I can compute the cross-product against the sparse rollups.
- [ ] I know what a new dimension costs and when the decision must be made.
- [ ] I know which number goes on the invoice and what I would alert on.
- [ ] I answered all three questions above out loud.
