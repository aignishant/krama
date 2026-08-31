---
day: 40
track: practice
title: "Practice — 2D prefix sums and inclusion-exclusion"
status: written
---

# Day 040 · Practice

**DSA topic:** 2D prefix sums and inclusion-exclusion
**System design topic:** Choosing SQL or NoSQL in an interview

---

## Code these, in this order

Four problems around one formula. **Before each, redraw the four-block picture** — in any tool
you like, or trace it in the air — and read the signs off it. The picture is the answer; the
formula is its transcript.

Before each one, ask:

1. Can I say the derivation? Big, minus strip above, minus strip left, plus the corner — why plus?
2. Where is the zero frame, and what size is the prefix table?
3. Which indices are matrix coordinates and which are prefix coordinates?
4. Is this a build question, a query question, or a loop-of-queries question?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Range Sum Query 2D — Immutable | LeetCode 304 (Medium) | The build and the four-term query, with the zero frame doing the edge work. |
| 2 | Matrix Block Sum | LeetCode 1314 (Medium) | A loop of O(1) queries with edge clamping — and keeping the two index worlds separate. |
| 3 | Count Square Submatrices with All Ones | LeetCode 1277 (Medium) | A ringer: it looks 2D-prefix-shaped and wants a different recurrence — route by structure. |
| 4 | Number of Submatrices That Sum to Target | LeetCode 1074 (Hard) | The composition: fix row pairs, collapse columns, run day 038's map on the 1D remainder. |

Problem 3 is the deliberate misfit again: prefix sums *can* verify squares, but the clean solution
is a different idea. Spend five minutes routing before committing.

### On problem 1, drop the plus-term on purpose

Query an interior region without `+ p[r1][c1]` and watch a wrong answer arrive with confident
arithmetic — on the lesson's matrix, region (2,1)-(4,3) returns 0 instead of 8. Then query a
region touching row 0 and see it come out *right* anyway. Say why edge regions hide this bug and
interior ones expose it.

### On problem 1 again, alias the rows

Build the table with `[[0] * (cols + 1)] * (rows + 1)` and print two entries from different rows
after one write. Same value. Name the day this trap first appeared, then rebuild with the
comprehension.

### On problem 2, police the index worlds

Say before coding: clamping happens in matrix coordinates (`max(0, r - k)`, `min(rows - 1, r + k)`),
the formula's `+ 1`s happen only inside the `prefix[...]` brackets. Confirm
`([[1,2,3],[4,5,6],[7,8,9]], 1)` gives `[[12,21,16],[27,45,33],[24,39,28]]`.

### On problem 4, name the composition first

One sentence before coding: "O(rows²) row pairs; for each, collapse to 1D column sums; then
day 038's seen-map with its `{0: 1}` sentinel counts subarrays summing to target." If the
sentence is right, the code is two tested pieces glued.

### The derivation drill

Out loud, from the picture, under thirty seconds each:

1. The query formula, with why each sign.
2. The build formula, with why its sign points the other way.
3. Nirmala's count: 42 students, 18 cricket, 15 football, 7 both — neither?
4. Integers under 100 divisible by 3 or 5.
5. Why does a query touching row 0 need no special case?

### The decision-procedure drill

Run the four questions — patterns, invariants, numbers, settledness — out loud for each system,
landing on a core plus carve-outs:

1. A hospital appointment system.
2. A multiplayer game's match telemetry (every player action, replay and analytics).
3. A note-taking app with offline sync.
4. An ad-click counting pipeline (billions of clicks, revenue reports).

### The challenge drill

One or two sentences each, out loud — the pushback answers:

1. "Just pick one store." — which, and why that one?
2. "We chose MongoDB because we might scale." — the two substitutions in that sentence.
3. "Your traffic grows 100×. What breaks first?" — the trigger numbers, in order.
4. "Why not put the analysts on the production database?" — whose copy, and what law applies?

### The arithmetic drill

From memory, in under two minutes:

- 1,000 × 1,000 matrix, 100,000 rectangle queries: re-summing vs per-row 1D prefixes vs 2D
  prefix — the three totals.
- A food-delivery app: 500k orders/day and 50k riders pinging every 3 s — which is inside one
  node and which is a firehose, with the per-second numbers.
- 2M sessions × 1 KB at 20k reads/s — the store, the size, and what it takes off the core.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Answer many rectangle-sum queries on a fixed matrix.*
   The stored object with its zero frame, the derivation from the picture with both signs
   explained, the build as the same law reversed, and the 1.4M-versus-10¹¹ arithmetic.

2. *SQL or NoSQL for this system, and what made you decide?*
   Refuse the binary; run the four questions on a system of your choosing; land on the core plus
   numbered carve-outs; close with what evidence would change your mind.

3. *Why do you add the corner back?*
   Inclusion-exclusion in one breath: removed twice, restored once — then the same law in two
   other costumes: the build step, and the divisible-by-3-or-5 count.

---

## Before you move on

- [ ] I can derive the four-term formula from the picture, signs included, without reciting.
- [ ] I can say why edge queries hide the missing-plus-term bug and interior queries expose it.
- [ ] I build 2D tables with a comprehension and a zero frame, reflexively.
- [ ] I can name the composition that solves submatrix-sum-to-target from two known tools.
- [ ] I can run patterns → invariants → numbers → settledness on an unseen system in two minutes.
- [ ] I have trigger numbers, not slogans, for when a path leaves Postgres.
- [ ] I answered all three questions above out loud.
