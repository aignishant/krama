---
day: 39
track: practice
title: "Practice — Difference arrays: range updates, cheaply"
status: written
---

# Day 039 · Practice

**DSA topic:** Difference arrays: range updates, cheaply
**System design topic:** Wide-column and time-series stores

---

## Code these, in this order

Four problems, one mechanic: two marks per update, one settle. **Before each, ask Sarasu's
question out loud** — is the end inclusive or exclusive, and therefore where does the minus go?

Before each one, ask:

1. Many range updates, one final report? (If reads interleave — wrong tool, say so.)
2. Inclusive end (`r + 1`) or exclusive end (`r`)?
3. How big is the coordinate space — dense array, or sorted map of marks?
4. Does the settle need the whole array, or just a running maximum / threshold check?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Range Addition | LeetCode 370 (Medium, premium — or code it from §5) | The pure pattern: two marks, extra slot, one settle. |
| 2 | Corporate Flight Bookings | LeetCode 1109 (Medium) | 1-indexed inclusive ends — deriving `diff[first-1]` and `diff[last]` instead of memorising. |
| 3 | Car Pooling | LeetCode 1094 (Medium) | The exclusive end — off *at* the stop — and the settle doubling as a capacity check. |
| 4 | Number of Zero-Filled Subarrays | LeetCode 2348 (Medium) | A cooldown problem: no difference array at all — proof you route by structure, not by phase. |

Problem 4 is a deliberate ringer: it says "subarrays" and "count", and it wants a run-length walk,
not today's tool. Route it honestly.

### On problem 1, size it wrong on purpose

Make `diff` exactly `length` long and apply an update ending at the last element. Collect the
`IndexError: list index out of range`, then say why `length + 1` slots removes the crash and the
guard at once.

### On problem 2, derive the indices aloud

Flights are 1-indexed, ends inclusive. Start from the 0-based rule — plus at start, minus past the
end — apply the shift, and watch the two off-by-ones cancel into `diff[last]`. Confirm
`([[1,2,10],[2,3,20],[2,5,25]], 5)` gives `[10, 55, 45, 25, 25]`.

### On problem 3, run the handover test

`[[2,1,5],[3,5,7]]` with capacity 3 — two off at stop 5, three on at stop 5. Correct code says
True. Now write the minus at `end + 1` and watch it say False. Say which convention this problem
uses and which line of the statement told you.

### On problem 3 again, the peak variant

Change the settle to track `peak = max(peak, riding)` and report the maximum riders instead of a
yes/no. One line — say why the running level already had the answer.

### The boundary drill

For each, say where the minus goes — `r` or `r + 1` — in under five seconds:

1. Add bonus marks to questions 3 through 7, inclusive.
2. Guests staying from day 2, leaving the morning of day 6.
3. Seats booked on flights 4 to 9, all flown.
4. A machine occupied from minute 10 until minute 25, freed at 25.
5. Discount applies from item index 0 to the last item.

### The routing drill

Which tool — difference array, prefix + map (day 038), window (day 032/034), or plain prefix
(day 037)? One sentence each:

1. Apply 10,000 range increments, then print the array.
2. Count subarrays summing to k, negatives allowed.
3. Answer 10,000 range-sum queries, array never changes.
4. Longest subarray with at most two distinct values.
5. Peak simultaneous meetings, given start and end times up to 10⁹.

Number 5 is today's tool in sparse clothing — say what replaces the dense array.

### The two-keys drill

For each query need, write the Cassandra-style key — `(partition key)` then clustering columns —
out loud:

1. Latest 50 messages in a channel.
2. A device's sensor readings for the last hour.
3. A user's orders, newest first — and the channel that never stops growing: what gets added to
   the partition key, and why?
4. All messages by one author across channels — and what does this question actually require?

### The metrics drill

Answer each in one or two sentences, out loud:

1. Why do fixed-interval timestamps compress ~50×, and which running trick from this phase is
   delta encoding?
2. Raw for 15 days, 5-minute averages for a year — what does this do to storage growth?
3. Why is retention-by-dropping-chunks cheap where a nightly `DELETE` is not?
4. When does TimescaleDB beat InfluxDB, and on what grounds?
5. What is a hot partition, and where does the fix live?

### The arithmetic drill

From memory, in under two minutes:

- 10,000 servers × 100 metrics × every 10 s — points/second and points/day.
- That day of points at ~100 bytes a row against ~2 bytes compressed.
- 1,000 updates averaging 50,000 wide on a 100,000-element array — naive writes against
  marks-plus-settle, and the measured ratio from the lesson.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Apply many range increments and then report the final array.*
   The two marks and why the untouched middle is free, the extra slot, the settle as day 037's
   prefix sum, the boundary question, and O(n + u) against O(n × u) with the measured ratio.

2. *Which database would you pick for storing metrics, and why?*
   Size the firehose first, then the three properties it forces, the two-part key, compression and
   retention with numbers, and the TimescaleDB / Prometheus / InfluxDB decision by context.

3. *What is Cassandra's data model, actually?*
   Partition key places — machine and bucket; clustering columns sort within; one table per query
   written at write time; the two key stress-tests — unbounded and hot partitions — and the
   promise the model demands.

---

## Before you move on

- [ ] I can write the two marks and the settle from memory, with the `length + 1` slot.
- [ ] I ask the inclusive-or-exclusive question on every range problem, and I can name the two
      problems that answer it differently.
- [ ] I know the contract — all updates, one settle, then reads — and the log-n trees to name when
      it breaks.
- [ ] I can switch the dense array for a sorted map when coordinates are huge.
- [ ] I can say Cassandra's two keys and their jobs, and design a message table key under stress.
- [ ] I can size a metrics firehose and defend a retention policy with arithmetic.
- [ ] I answered all three questions above out loud.
