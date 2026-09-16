---
day: 41
track: practice
title: "Practice — Prefix sums revision and mock round"
status: written
---

# Day 041 · Practice

**DSA topic:** Prefix sums revision and mock round
**System design topic:** Connection pools, ORMs, and the N+1 query

**Theme:** Dates, times, and randomness

---

## Code these, in this order

A mock, so the protocol rules: **thirty-five minutes a problem, standing, talking, nothing
open — and Rekha's pencil minute first.** Name the chapter and the tell before solving anything.
Score yourself against §5 of the lesson on the naming, before the code.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Find the Highest Altitude | LeetCode 1732 (Easy) | The warm-up: running prefix in one variable, sentinel 0 as the starting altitude. |
| 2 | Product of Array Except Self | LeetCode 238 (Medium) | Whether the prefix instinct survives a change of operation — and why division is banned. |
| 3 | Continuous Subarray Sum | LeetCode 523 (Medium) | The remainder disguise, the frozen first-index map, and the length-2 rule. |
| 4 | Range Sum Query 2D — Immutable | LeetCode 304 (Medium) | The phase's four-corner summit, re-derived cold a day later. |

### On problem 1, respect the warm-up

One pass, one variable, track the maximum — and say where the sentinel is (the starting altitude
0 counts, and it can be the answer). If this takes more than ten minutes, the phase needs
re-reading, not more problems.

### On problem 2, crash the shortcut first

Write the division version and run it on `[-1, 1, 0, -3, 3]` — collect the
`ZeroDivisionError: integer division or modulo by zero`. Then say the deeper reason the ban
exists — subtraction always has an inverse, division does not — and write the two-sweep version.
Say "O(1) extra space beyond the output" in exactly those words.

### On problem 3, run the punishing inputs

After your solution passes the samples, run the four from the lesson: `[0, 0]` with k = 1
(True — zero is a multiple), `[6]` with k = 6 (False — length rule), `[5, 0, 0, 0]` with k = 3
(True — and the input that catches an overwritten first index), `[1, 0]` with k = 2 (False).
If any surprises you, say which of the five pre-flight bugs it maps to.

### On problem 4, derive from the picture again

No peeking at day 040: draw the four blocks in any tool, read off the signs, then code. The test
of yesterday is whether the derivation — not the formula — survived the night.

### The pre-flight drill

Say the five bugs of the phase from memory, each with its checking input or symptom:

1. The sentinel (which four costumes has it worn?).
2. Ask-then-record (which k checks it?).
3. The boundary — minus at `r` or `r + 1` (which two problems answer differently?).
4. The map's contract — count or frozen first-index (which question picks which?).
5. The index that reaches −1 (what does Python do instead of crashing?).

### The chapter-naming drill

Name the tool — or the exit — for each, in under ten seconds:

1. Answer 100,000 range-sum queries on a fixed array.
2. Count subarrays summing to k, negatives allowed.
3. Apply 10,000 range increments, then print the array.
4. Rectangle sums on a fixed matrix.
5. Longest subarray with sum at most k, all positive.
6. Range sums with updates arriving between queries.
7. Does a subarray of length ≥ 2 sum to a multiple of k?
8. Product of the array except self, no division.

Numbers 5 and 6 are exits — name where each goes.

### The N+1 drill

Answer each in one or two sentences, out loud:

1. What does the N+1 signature look like in a query log?
2. Why is 101 × 1 ms slow when the database is fast? (The sentence about conversation turns.)
3. Which eager-loading flavour for to-one, and which for to-many — and why the difference?
4. Name the three structural guard rails, cheapest first.
5. Why does N+1 never appear in a query plan, and which day taught that?

### The pool drill

From memory, in under two minutes:

- What opening a Postgres connection costs — the three steps and the process — and what a pool
  lease costs instead.
- The pool-size starting rule for an 8-core database, and why a pool of 200 helps nothing.
- 500 instances × 20 connections against `max_connections = 100` — the tool, and the session
  state its transaction mode trades away.
- The hub page at 200 req/s: lazy versus eager queries per second, and the sentence about
  "we outgrew Postgres" stories.

### The phase-closing drill

The database phase ends next lesson-block. Say the one-line cost of each tool from the phase's
recall cards — prefix array, prefix + map, difference array, 2D prefix — then the four-question
store-choosing procedure from day 040, then the N+1 fix. Under three minutes, standing. That is
the phase, portable.

---

## Build these, in all three languages

Build each exercise in Python, Go, and C++. Use today's lesson programs as the
starting point; use OpenSSL for secure bytes in C++.

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Display a meeting at 2026-01-15 10:00 UTC in Asia/Kolkata; expect 15:30 on the same date. | Converting one instant with named zone rules rather than relabelling its hour. |
| 2 | Time a sum of 0 through 999 using the monotonic clock, then report milliseconds with explicit units. | Separating an event timestamp from elapsed time; the sum must be 499500 and the duration nonnegative. |
| 3 | Generate 16 secure bytes and encode them as 32 hex characters; separately replay two identically seeded simulation generators. | Secure randomness versus repeatability; check failures and never print an actual reset token. |

For exercise 1 in C++, use the lesson's C++20 zone fragment with a library supporting
time zones and an installed zone database. Report a missing dependency explicitly;
do not replace a named zone with a fixed offset and claim the general problem solved.
For exercise 2, also calculate a simulated wall difference from readings 100 and 95:
it is -5 seconds, demonstrating why corrected wall time cannot time your database call.

## Compare

Write one sentence for each language after running the exercises:

- **Python** — Explain why datetime, time.monotonic, and secrets have separate jobs.
- **Go** — Explain what time.Now retains and what serialising a time loses.
- **C++** — Explain the duration units and which dependencies provide zones and secure bytes.

## Say these out loud

### DSA and system design

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Product of the array except self — no division allowed. Why not, and what instead?*
   The inverse argument, the zero crash, the two sweeps with the multiplicative sentinel, and
   the space claim said precisely.

2. *Your page makes 200 database calls per request. What happened?*
   Diagnose from the shape, name lazy loading, fix with the right eager-loading flavour, add the
   guard rails, and check the pool underneath — the full model answer, compressed.

3. *Does the array contain a subarray of length at least two summing to a multiple of k?*
   The remainder tell, the frozen first-index map with its `{0: -1}` sentinel, the derived
   length rule, and the input that punishes an overwritten index.

### Languages

Answer each in two minutes, standing up, without notes.

1. Why should you not use the wall clock to measure elapsed time?
2. Why is 10:00 UTC the same instant as 15:30 in Kolkata on the example date?
3. Why is a seeded simulation generator unsuitable for a reset token?


## Before you move on

- [ ] I did all four problems with the pencil minute first, and scored the naming separately.
- [ ] I can recite the five pre-flight bugs with their checking inputs.
- [ ] I can name the chapter for all eight drill phrasings, including both exits.
- [ ] I can tell the N+1 story end to end: signature, mechanism, fix, guard rails.
- [ ] I can do the pool arithmetic — opening cost, sizing rule, fleet multiplication — from
      memory.
- [ ] I can deliver the phase-closing drill in under three minutes.
- [ ] I answered the DSA, system design, and language questions out loud.
- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I converted the fixed meeting correctly in all three languages.
- [ ] I measured elapsed time with a monotonic clock and named its units.
- [ ] I generated secure bytes, checked failures, and explained why encoding adds no randomness.
